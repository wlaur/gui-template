import sys
import ctypes


from PyQt5.QtWidgets import (QMainWindow,
                             QLabel,
                             QStatusBar)

from gui_template.helper import set_stylesheet, set_window_icon
from gui_template.interface import MyTabWidget
from gui_template.settings import APP_NAME, VERSION


class MyMainWindow(QMainWindow):

    def __init__(self, parent=None, app=None):
        """
        class for the main window

        this only contains one widget, the TabWidget

        all actions are defined in that class, this class only handles
        things that explicitly have to do with the window, e.g. closeEvent
        """

        super().__init__(parent)

        self.app = app
        self.resize(900, 800)

        # everyone should have at least this resolution heheh
        self.setMinimumSize(900, 800)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        # this is a QLabel that is added to the right side of the statusbae
        self.statusbar_right = QLabel('')
        self.statusbar.addPermanentWidget(self.statusbar_right)

        self.setTitle(f'{APP_NAME} {VERSION}')

        self.tab = MyTabWidget(self)
        self.setCentralWidget(self.tab)

    def setTitle(self, text):

        self.title = str(text).strip()
        self.setWindowTitle(self.title)

    def setStatus(self, text, side='left'):

        if side == 'left':
            self.statusbar.showMessage(text)

        elif side == 'right':
            self.statusbar_right.setText(text)

    def closeEvent(self, event):
        # save settings on close, just to be sure
        self.tab.settings.save()
        return super().closeEvent(event)


def GUI(app, splash):
    """
    sets up the GUI

    takes the app and splash screen as arg, to be able to close it after
    the GUI setup is finished
    """

    # this is needed to show the taskbar icon in windows, and to give
    # the process the correct name
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_NAME)

    set_stylesheet(app)

    window = MyMainWindow(app=app)
    set_window_icon(app)

    window.show()

    # remove splashscreen
    splash.finish(window)

    print('successfully initialized GUI')

    sys.exit(app.exec_())
