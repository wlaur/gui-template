import os
import datetime
from pathlib import Path

from typing import Iterator, Union
from collections.abc import Iterable


def get_file_size(path: Union[Path, str], unit='MB') -> float:
    """
    get the file size of file at path, in MB (default)
    """

    size_bytes = os.path.getsize(path)

    if unit == 'B':
        size = size_bytes
    elif unit == 'KB':
        size = size_bytes / 1024
    elif unit == 'MB':
        size = size_bytes / (1024 * 1024)
    elif unit == 'GB':
        size = size_bytes / (1024 * 1024 * 1024)
    else:
        raise ValueError(f'unit {unit} not recognized')

    return float(size)


def is_null(x) -> bool:
    """
    determines which if input x is a representation of a NULL / missing / NaN / None value

    NOTE: this function does not consider empty string or string of only whitespace to be null

    NOTE: the python sqlite3 library uses None as null representation (e.g. return values from fetchall)

    accepted NULL-representations:
        np.nan, float('NaN'), "NaN"
        None
        'Null', 'NULL', 'null' (not case-sensitive)
        '[EMPTY]' (case-sensitive)
    """

    # allow 0.0 and 0 and all other numerical values
    if isinstance(x, (float, int)):
        return False

    # passing NaN or None returns True
    if x != x or x is None:
        return True

    # "null" (not case-sensitive)
    if isinstance(x, str) and x.lower() == 'null':
        return True

    # "NaN" (case-sensitive)
    if isinstance(x, str) and x == 'NaN':
        return True

    # "[EMPTY]" (case-sensitive)
    if isinstance(x, str) and x == '[EMPTY]':
        return True

    return False


def clean_sqlite_string(x) -> str:
    """
    cleans a string for use with SQLite
    converts to string, and surrounds with single quotes

    escapes single quotes by placing a second single quote before it
    double quotes inside the string are not changed

    NOTE: will not strip whitespace
    """

    x = str(x)

    # replace single quotes with 2 pcs to escape them
    x = x.replace("'", "''")

    # return the value surrounded by single quotes
    return f"'{x}'"


def divide_chunks(container: Iterable, N) -> Iterator[object]:
    """
    generator that divides container into chunks of N
    the last chunk might not have N elements

    usage:
        parts_with_3_elements = list(divide_chunks(container, 3))
    """

    for i in range(0, len(container), N):
        yield container[i:i + N]


def flatten(container: Iterable, max_depth=None, depth=0) -> Iterator[object]:
    """
    generator that yields elements

    usage:
        flat_list = list(flatten(nested_list))

    flatten arbitrarily deeply nested lists or tuples
    if max_depth=None, flatten until no more nesten structures remain
    otherwise flatten until specified depth

    NOTE: uses isinstance(obj, collections.abc.Iterable) to determine whether to recurse deeper
          strings are not considered iterables
    """

    if max_depth is not None and depth >= max_depth:
        yield container

    depth += 1

    for i in container:
        if isinstance(i, Iterable) and not isinstance(i, str):
            for j in flatten(i, max_depth=max_depth, depth=depth):
                yield j
        else:
            yield i


def get_display_str(s) -> str:
    """
    returns a display string for s, which is limited to a single line

    replaces \n with &n, to avoid newlines to be printed
    replaces \r with &r to avoid returning to start of line
    replaces \t with &t to avoid whitespace
        still allows multiple spaces

    * if s is empty string: return "[EMPTY STRING]"
    * if s is None (Python object): return "[None]"
    * if s is np.nan, NaN, float(nan): return "[NaN]"
    * if s.strip() == '', return "[WHITESPACE]" (for example: space, \t, \n)

    otherwise return input (as string)
    non-str objects will be converted to string (using str())
    """

    if s is None:
        return '[None]'

    # np.nan, float('NaN')
    if s != s:
        return '[NaN]'

    # ensure that s is str
    if not isinstance(s, str):
        s = str(s)

    if s == '':
        return '[EMPTY STRING]'

    if s.strip() == '':
        return '[WHITESPACE]'

    # replace newline, return to start and tab
    s = str(s).replace('\n', '&n')
    s = str(s).replace('\r', '&r')
    s = str(s).replace('\t', '&t')

    return s


def is_numeric(x) -> bool:
    """
    checks whether the input can be convert to float
    uses try / except
    """

    try:
        float(x)
        return True
    except Exception:
        return False


def convert_to_numeric(x: str) -> Union[int, float]:
    """
    convert input string to integer or float if it is a string
    representation of that

    this function can return:
        int
        float
        NaN (type float)
        str (in case string is not numeric)

    input that is not string or (float, int) will return 0

    returns int in case the value is exacly an integer value
    '1.000' → integer 1
    also convert floats to int according to this
    """

    if not isinstance(x, str):

        if isinstance(x, (float, int)):

            # return int if the value is an integer
            if int(x) - x == 0:
                return int(x)

            return x

        return 0

    x = x.strip()

    if is_numeric(x):

        x = float(x)

        # the builtin float function can convert string "NaN" to float(NaN)
        if x != x:
            return x

        # use int in case the value is an integer value
        if float(x) - int(x) == 0:
            x = int(x)

    return x


def ticks_to_date(ticks) -> datetime.datetime:
    """
    converts C# / .NET ticks to
    python datetime, removing milliseconds
    """

    delta = datetime.timedelta(microseconds=int(ticks) / 10)

    return (datetime.datetime(1, 1, 1) + delta).replace(microsecond=0)
