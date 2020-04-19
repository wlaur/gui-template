import os
import sys

from pathlib import Path
import fire
import shutil
from distutils.dir_util import copy_tree
import getpass
import time
import datetime
import pkg_resources


# increment manually
VERSION_MAJOR = '0'
VERSION_MINOR = '1'


USER = getpass.getuser()

# this will be removed after the installer is created
build_path = Path(os.path.expandvars(r'%UserProfile%\Desktop'))
project_path = Path('.').absolute()

# this path must be without spaces, since there are double quotes in the arg to ISCC.exe
# spaces in paths would normally be surrounded by double quotes
# the windows commandline cannot handle this many quotes!
innosetup_path = 'ISCC'

env_path = Path(os.path.expandvars(
    r'%APPDATA%\Local\Continuum\anaconda3\envs\minimal'))


# innosetup_path cannot contain spaces since there are double quotes in the argument
# use this portable installation of InnoSetup
# https://github.com/JeremyLee/portable-innosetup
# for some reason, the official installation of InnoSetup produces installers with
# access denied errors at the end of setup (does not impact installations)
if ' ' in str(innosetup_path):
    raise EnvironmentError('the path to ISCC.exe must be without spaces')


# cases with specific settings to be able to compile with nuitka
# key: name of case
# val: command, list of files to copy to dist folder [(orig, dest)]
# NOTE: limit the number of dependences to keep file sizes low
# http://manpages.ubuntu.com/manpages/trusty/man1/nuitka.1.html
CASES = {
    'pyqt':
    (
        'python -m nuitka '
        '--standalone '
        '--windows-disable-console '
        '--remove-output '
        '--python-flag=nosite '
        '--recurse-all '
        '--show-progress '
        # this is needed to enable the "modern" style for Qt
        '--plugin-enable=qt-plugins=sensible,styles '
        f'--windows-icon="{project_path / "assets/app-icon.ico"}"',
        [
            (project_path / 'assets', 'assets'),
            (project_path / 'data', 'data'),
            # needed for pywin32, pywintypesXX.dll is copied for some reason, but not pythoncomXX.dll
            # XX is 37 for Python 3.7, tried to make this work also with other versions
            # (env_path / f'Lib/site-packages/pywin32_system32/pythoncom{sys.version_info.major}{sys.version_info.minor}.dll',
            #  f'pythoncom{sys.version_info.major}{sys.version_info.minor}.dll')
        ]
    )
}


def get_package_version(package):
    return pkg_resources.get_distribution(package).version


def get_gcc_version():

    ret = os.popen('gcc.exe --version').read()

    # return the first line
    return ret.split('\n')[0].strip()


def get_build_info(t):

    # write version number, build system, username and timestamp to the data/build.txt file
    # need to do this before copying the data folder to the dist folder
    timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
    month_year = datetime.datetime.now().strftime('%B %Y')

    packages = ['PyQt5', 'qdarkstyle', 'xlrd', 'xlsxwriter', 'fire', 'pywin32']

    packages_str = '\n'.join(
        [f'{n}: {get_package_version(n)}' for n in packages])

    # written to data/build.txt, also loaded in the Instructions tab in the software
    build_info = f"""Version {VERSION_MAJOR}.{VERSION_MINOR}
{month_year}

Built using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} and nuitka {get_package_version('nuitka')}
compiler: {get_gcc_version()}

Built on {timestamp}
by user {USER} in {t:.0f} sec

Packages:
---------
{packages_str}
"""
    return build_info


def create_installer(dist_name):

    # this file has rows
    # AppVersion={APPVERSION}
    # Source: "{BUILD_DIR}\app.exe"; DestDir: "{app}"; Flags: ignoreversion
    # Source: "{BUILD_DIR}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
    with open('tools/installer-orig.iss', 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace('{BUILD_DIR}', str(
        build_path.absolute()) + '\\' + f'{dist_name}.dist')

    text = text.replace('{APPVERSION}', f'{VERSION_MAJOR}.{VERSION_MINOR}')

    if os.path.isfile('tools/installer.iss'):
        os.remove('tools/installer.iss')

    with open('tools/installer.iss', 'w', encoding='utf-8') as f:
        f.write(text)

    # output to installer folder
    # this must be run from root of project
    cmd = f'{innosetup_path} /O"./installer" tools/installer.iss'
    os.system(cmd)


def compile_app(input_file='app.py', case='pyqt', remove_dist=False):

    # need to get absolute path here since os.chdir(build_path) is called later
    input_file = Path(input_file).absolute()

    path_string = str(input_file)

    if os.path.isfile(project_path / 'data/settings.txt'):
        os.remove(project_path / 'data/settings.txt')

    # need to start to generate settings.txt, need to close window to continue compilation
    os.system(f'python "{input_file}"')

    if case not in CASES:
        print(
            f'case {case} not found, available: {", ".join(list(CASES.keys()))}')
        return

    cmd, files = CASES[case]

    # add the file name as last arg to nuitka
    cmd += f' "{path_string}"'

    os.chdir(build_path)

    # this folder will be created by nuitka
    output_dir = build_path / f'{input_file.stem}.dist'

    t0 = time.perf_counter()

    # NOTE: a C++ compiler needs to be in the PATH
    # for Visual studio, run "vcvarsall x64" to add the compiler to PATH
    os.system(cmd)

    # seconds
    t = time.perf_counter() - t0

    build_info = get_build_info(t)
    build_info_path = input_file.parent / 'data/build.txt'

    with open(build_info_path, 'w') as f:
        f.write(build_info)

    # remove log before copying
    # NOTE: don't remove settings.txt, there needs to be an updated
    # settings.txt in the installer, otherwise it might use an older, invalid file
    # delete settings.txt and run the app once to generate a new settings.txt
    # with default settings

    if os.path.isfile(project_path / 'data/log.txt'):
        os.remove(project_path / 'data/log.txt')

    # in case files/folders need to be manually included in the dist folder
    if files:
        for orig, dest in files:

            dest = output_dir / dest

            # if orig is a directory, copy directory and all contents
            if os.path.isdir(orig):
                copy_tree(str(orig), str(dest))

            # else, only copy the file
            else:
                # make a subdir in the dist folder in case it does not exist
                if not os.path.isdir(dest.parent):
                    os.mkdir(dest.parent)

                # copy with no metadata
                shutil.copyfile(orig, dest)

    # change back to project path to make the installer
    os.chdir(project_path)

    # use innosetup to create an installer from app.dist
    create_installer(input_file.stem)
    print('created installer')

    if remove_dist:
        # remove the dist folder
        shutil.rmtree(output_dir)
        print('removed dist folder')


def ui_convert():

    ui_path = Path('gui_template/ui')

    for n in os.listdir(ui_path):

        fp = ui_path / n

        out = ui_path.parent / f'{fp.stem}_form.py'

        cmd = f'pyuic5 -o {out} {fp}'
        print(cmd)
        os.system(cmd)


def main(inp):

    if inp == 'ui':
        ui_convert()

    elif inp == 'compile':
        compile_app()

    else:
        raise ValueError(f'unknown command {inp}')


if __name__ == '__main__':

    fire.Fire(main)
