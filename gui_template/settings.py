import os
import json


from gui_template.io import load_json

APP_NAME = 'App Name'

SETTINGS_PATH = 'data/settings.txt'
BUILD_PATH = 'data/build.txt'


# read the version number from the build.txt file (first row)
if os.path.isfile(BUILD_PATH):
    with open(BUILD_PATH, 'r', encoding='utf-8') as f:
        VERSION = f.read().split('\n')[0].split('version')[-1].strip()
else:
    VERSION = ''


def get_default_settings() -> dict:
    return {}


class Settings:

    def __init__(self, parent, file_path=None):
        """
        keeps track of all settings, saves to data/settings.txt

        connect GUI elements to the load/save methods of this class
        """

        self.parent = parent
        self.file_path = file_path
        self.ui = self.parent.ui

        self.sdict = {}

    def load(self):

        if os.path.isfile(self.file_path):

            # this function checks other encodings that utf-8 if necessary
            self.sdict = load_json(self.file_path)
        else:
            self.sdict = get_default_settings()

    def save(self):

        if not self.sdict:
            return

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.sdict))
