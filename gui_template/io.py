import os
import shutil
import sqlite3
import datetime
import json

from pathlib import Path
from typing import Union

# tries to open files using these encodings, in order
# break loop if the operation using the loaded data succeeded
# this is not fool-proof, should use something like chardet to
# detect endcodings in case this becomes an issue
# NOTE: ANSI means default encoding for the system:
# cp1252 for Windows using western languages
POSSIBLE_ENCODINGS = ['utf_8', 'utf_8_sig',
                      'utf_16_be', 'utf_16_le', 'utf_16',
                      'ascii', 'cp1252']


def load_json(path: Union[Path, str]) -> object:
    """
    reads a .json file and returns the object
    from json.load(file)

    Returns False in case the file could not be loaded using
    any of the encodings listen in io.POSSIBLE_ENCODINGS

    Parameters
    ----------
    path : Union[Path, str]
    """

    for enc in POSSIBLE_ENCODINGS:
        with open(path, encoding=enc) as f:

            try:
                return json.loads(f)
            except:
                continue

    return False


def last_modified(path: Union[Path, str], prefix='modified: ') -> str:
    """
    returns a string when path was last modified
    with prefix, default "modified: "

    uses os.path.getmtime to get the timestamp
    and datetime.datetime.fromtimestamp to get a time string
    """

    ts = os.path.getmtime(str(path))
    time_str = datetime.datetime.fromtimestamp(
        ts).strftime('%d-%m-%Y %H:%M:%S')

    return f'{prefix}{time_str}'


def has_changed(path: Union[Path, str], last: str) -> bool:
    """
    Checks if path has changed on disk.
    last is the previous timestamp to compare with.
    """

    return last_modified(path, prefix='') != last


def is_local_path(path: Union[Path, str]) -> bool:
    """
    checks whether path is located on the computer (i.e. HDD)
    or on a network drive

    assumes that C and D are local HDDs, all other drives are remote
    or USB or similar
    this is maybe not 100% correct, but cannot find a
    consistent way to check this, don't want to call `net use`
    and parse output...

    path can be a folder or a file
    """

    # this works for both Path and str
    # Z:\NETWORK DRIVE\folder\etc → Z
    # C:\Users\user\folder\etc → C
    path_drive_letter = str(path)[0]

    if path_drive_letter in ('C', 'D'):
        return True

    return False


def process_input(args, ext='') -> tuple:
    """
    returns a list of absolute file paths (WindowsPath objects) and the
    folder as WindowsPath object in which the last file is located
    (since the input files might be in different folders)

    works with both a directory and file path(s) as input
    (space-separated in command line in case several paths are given)
    in case of a directory, includes all files with
    extension ext (can be tuple of strings), default '' (all files)


    usage:
        fnames, directory = process_input(args, ext=('.pdf', '.xlsx'))

    args:
        args: path to a directory (1-tuple) *or* list of
        file paths (N-tuple) (from commandline args)
        ext: list of file extensions to include (empty string includes all files)

    returns:
        fnames: list of absolute filepaths as WindowsPath objects
        folder: directory of the _last_ given input as a WindowsPath object
    """

    if isinstance(args, str):
        args = (args, )

    # if a directory is given as input, list all files with extension in that directory
    if os.path.isdir(args[0]):

        folder = Path(args[0])
        fnames = [Path(folder / a).absolute()
                  for a in os.listdir(folder) if a.endswith(ext)]

    # if one or multiple file paths are given as input, create WindowsPath objects from them
    else:
        fnames = [Path(a).absolute() for a in args if a.endswith(ext)]

        # this will refer to the _last_ input path folder in case files from different folders are passed
        folder = Path(args[0]).parent

    return fnames, folder


class DatabaseHandler:

    def __init__(self, path, callback=None, progress=None):
        """
        loads a SQLite database file and keeps it in memory

        NOTE: it is important that this class works as intended
              also in case the files are located on network drives
              the user might have a bad network connection, which
              can lead to a number of issues in common file operations
              like remove, copy, etc...

        if progress is not None, it is passed to the sqlite3.connection.backup method

        callback is called each time an SQL statement is executed on the in-memory database

        progress is a callable object that will be executed at each iteration
        with three integer arguments: status of the last iteration, the remaining number of pages
        still to be copied and the total number of pages.

        seems like windows has some type of cache for files on
        network drives, the second time a file is opened it's much faster
        also seems to work if the file is modified, hopefully windows manages this correctly
        """

        self.progress = progress
        self.callback = callback

        # these settings for connection.backup updates the progressbar more smoothly
        self.pages = 100
        # this setting does not seem to do anything?
        self.sleep = 0

        # create a new database connection in memory
        # note: there can only be one connection to this database
        # ensure that any previous connections to this in-memory database have been closed
        # (effectively deleting any previous data)
        self.connection = sqlite3.connect(':memory:')

        if self.callback is not None:
            self.connection.set_trace_callback(self.callback)

        # path to the SQLite datbase file
        self.path = Path(path).absolute()

        self.load()

    def load(self) -> None:
        """
        load a SQLite database from a file and read it
        into the in-memory SQLite db

        if the file is on a network drive, reading it into
        memory might take a while

        use the progress callback to monitor progress, by default
        the file is read in 100 parts with a callback after each
        """

        # connect to the SQLite database at path
        source = sqlite3.connect(str(self.path))

        # copy the contents of source into the in-memory db
        # do this in steps of 100, otherwise it is slower for some reason
        source.backup(self.connection, pages=self.pages, sleep=self.sleep,
                      progress=self.progress)

    def save(self):
        """
        dumps the in-memory datbase to disk, overwriting the original database file

            this method calls connection.commit()

        creates a backup of the original file

        NOTE: this method does _not_ close the database connection
        it must be closed by the user if necessary

        raises PermissionError in case the file cannot be written to
        """

        # the backup file will be prefixed with "backup-"
        backup_path = self.path.parent / f'backup-{self.path.name}'

        # check that the user has write permissions for both the original and backup files
        # this file must exist
        if not os.access(self.path, os.W_OK):
            raise PermissionError(f'no write permission for {self.path}')

        # this file might not exist, if it does, check permissions
        if os.path.isfile(backup_path) and not os.access(backup_path, os.W_OK):
            raise PermissionError(f'no write permission for {backup_path}')

        # if an older backup file already exists, remove it
        # NOTE: running 2 subsequent update operations means
        # that all original data is lost, since the second update operation
        # will overwrite the backup. This backup is only used in case the
        # program fails during the update operation
        # this should not happen, since sqlite_instance exception handling will
        # ensure that the file is not written in case of an exception (at
        # least in case of a SQL-related exception)
        # if _this_ method fails, there might be more problems!
        if os.path.isfile(backup_path):
            os.remove(backup_path)

        # this saves everything that has been done to the database
        # NOTE: this only saves to the in-memory database
        self.connection.commit()

        # copy the original file to the backup path, and remove the original file
        shutil.copy2(self.path, backup_path)

        # the in-memory database must be written to file
        # create a new, disk-based connection and backup the in-memory db to this
        file_connection = sqlite3.connect(str(self.path))

        # write the in-memory database to disk
        # this will overwrite existing data in the SQLite file,
        # however it does not overwrite the _entire_ file
        # in case the target file is on a network, any number of things
        # can go wrong (due to bad network connections)
        # see https://www.sqlite.org/howtocorrupt.html for some examples
        # let's just hope this will always work, if it does not
        # the entire project can become unusable
        # all metadata is still present embedded into the dwgs,
        # so in that case the project can be recreated (using
        # the same project setup template)
        # will wrap this in a try-except, assuming sqlite3 will raise
        # some exception if the write fails due to bad network
        try:
            self.connection.backup(file_connection, pages=self.pages, sleep=self.sleep,
                                   progress=self.progress)
            failed = False

        except Exception as e:

            failed = True
            raise e

        finally:

            if failed:
                # if this fails, copy the backup to 3rd file to
                # avoid it being overwritten in case the user tries the
                # update again. If the user has network problems
                # this will likely also fail
                shutil.copy2(backup_path, self.path.parent /
                             f'backup-2-{self.path.name}')
                print('copied backup to backup-2')
