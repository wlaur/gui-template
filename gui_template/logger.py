import os
import sys
import re
import logging

import logging.config


LOG_PATH = 'data/log.txt'
LOG_LEVEL = 'info'

# disable all loggers from previously imported packages
# NOTE: if something is imported _after_ this is executed, it will not be disabled
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True
})

logger = logging.getLogger()

# remove the old log file, otherwise it will grow each time the application is run
if os.path.isfile(LOG_PATH):

    try:
        os.remove(LOG_PATH)
    except:
        pass


if LOG_LEVEL == 'error':
    level = logging.ERROR

elif LOG_LEVEL == 'warn':
    level = logging.WARN

elif LOG_LEVEL == 'info':
    level = logging.INFO

elif LOG_LEVEL == 'debug':
    level = logging.DEBUG


# log is outputted (appended) to data/log.txt
logging.basicConfig(stream=open(LOG_PATH, 'a', encoding='utf-8'),
                    format='%(asctime)-15s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=level)


COLORS = {'blue': '#6efae0',
          'orange': '#ffc757',
          'red': '#ff0000',
          'grey': '#adadad',
          'white': '#ffffff',
          'green': '#556b2f',
          'yellow': '#e0f23f'}


def color_line_segment(segment, color):
    return f'<span style="color:{color}">{segment}</span>'


def process_log_line(line: str) -> str:
    """
    adds color and other rich text formatting to the log message
    this function is called for each line in data/log.txt when the
    log textbrowser is initialized
    """

    if 'ERROR' in line:
        color = COLORS['red']

    elif 'WARNING' in line:
        color = COLORS['orange']

    elif 'INFO' in line:
        color = COLORS['blue']

    elif 'DEBUG' in line:
        color = COLORS['yellow']

    else:
        return ''

    pattern = re.compile(r'INFO|WARNING|ERROR|DEBUG')

    # find the start, end index of INFO, WARNING, DEBUG or ERROR
    a, b = pattern.search(line).span()

    space_str = '&nbsp;'

    timestamp = line[:a].strip()
    timestamp_str = color_line_segment(f'<i>{timestamp}</i>', COLORS['grey'])

    level = line[a:b].strip()

    level_str = color_line_segment(f'<b>{level}</b>', color)

    # timestamp_str is always the same length, level changes
    part1 = f'{timestamp_str}{space_str}{level_str}'

    n_spaces = 28 - b
    spaces = space_str * n_spaces

    msg = line[b:].strip()

    msg_str = color_line_segment(msg, COLORS['white'])

    rich_text_line = f'{part1}{spaces}{msg_str}'

    return rich_text_line


class StreamToLogger:
    """
    Fake file-like stream object that redirects writes to a logger instance
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():

            if not line.rstrip():
                continue

            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


# want to redirect print calls to logger
# still keep the print calls in the sql.py functions, since this
# module is can also be imported to other environments (where print to stdout is expected)
sys.stdout = StreamToLogger(logger, log_level=logging.INFO)
