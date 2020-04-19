from PyQt5.QtWidgets import QWidget, QFileDialog
from pathlib import Path


class BrowseDialog(QWidget):

    def __init__(self, parent=None) -> None:
        """
        class that shows a folder/file browse window and returns the
        selected folder/file as Path


        the filter_str specifices which file types are visible and selectable

            Images (*.png *.xpm .jpg)
            JSON (*.json)
            Excel files (*.xlsx *.xlsm *.xls)
        """

        super().__init__(parent)

    def getDirectory(self, start_path='.') -> Path:
        """
        returns a single absolute directory path
        returns None if the window is closed before anything is selected
        """

        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(
            self, options=options, directory=start_path)

        if directory:
            return Path(directory).absolute()

        return None

    def getFile(self, title='Open...', filter_str='JSON (*.json)', start_path='.') -> Path:
        """
        returns a single absolute filepath
        returns None if the window is closed before anything is selected
        """

        # returns path, filter
        files = QFileDialog.getOpenFileName(
            self, title, start_path, filter_str)

        # return None if the window was closed
        if not files[0]:
            return None

        return Path(files[0]).absolute()

    def getMultipleFiles(self, title='Open...', filter_str='JSON (*.json)', start_path='.') -> list:
        """
        returns a single absolute filepath
        returns None if the window is closed before anything is selected
        """

        # returns list[path], filter
        files = QFileDialog.getOpenFileNames(
            self, title, start_path, filter_str)

        # return None if the window was closed
        if not files[0]:
            return None

        return [Path(n).absolute() for n in files[0]]

    def saveFileAs(self, title='Save as...', filter_str='JSON (*.json)', start_path='.') -> Path:
        """
        returns a single absolute filepath
        returns None if the window is closed before anything is selected
        """

        files = QFileDialog.getSaveFileName(
            self, title, start_path, filter_str)

        # return None if the window was closed
        if not files[0]:
            return None

        return Path(files[0]).absolute()
