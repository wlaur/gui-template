from PyQt5.QtWidgets import QTabWidget, QDialog
from PyQt5.QtCore import Qt

from gui_template.interface_form import Ui_TabWidget
from gui_template.dialog_form import Ui_Dialog
from gui_template.progress import progress


from gui_template.helper import populate_table
from gui_template.folderdialog import BrowseDialog
from gui_template.settings import (SETTINGS_PATH,
                                   Settings)

# this import redirects stdout to logging.INFO
# and stderr to logging.ERROR
# can just use print in the code,
#  no need to explicitly call logger.info()
# this import should be the last import to prevent other modules from
# outputting to logger
from gui_template.logger import LOG_PATH, process_log_line


class SeparateWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.parent = parent

        # don't allow focus outside this window
        self.setModal(True)

        # disable the X close button
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # remove questionmark from title bar
        self.setWindowFlags(
            self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        self.setWindowTitle('Separate dialog')

        self.ui.CloseButton.clicked.connect(self.close)

    def closeEvent(self, event):

        event.accept()


class MyTabWidget(QTabWidget):

    def __init__(self, parent=None, app=None):
        """
        class for the TabWidget, which is the only widget in the main window

        * all actions are defined as methods in this class
        * UI elements are accessed using the ui attribute

        NOTE: no threading is used in this application.
        Processes that take more time will have a modal progressbar to
        prevent access to the GUI while the program is busy

        TODO: there are many methods in this class,
        maybe split up into multiple classes?
        """
        super().__init__(parent)

        self.window = parent
        self.app = parent.app

        # might need to access this TabWidget via the MainWindow
        self.window.tab = self

        # the basic look and layout is defined in interface_form.py
        # which is generated from ui/interface.ui,
        # which is created using Qt Designer
        self.ui = Ui_TabWidget()
        self.ui.setupUi(self)

        # this handles the tab change actions
        # need to keep track of which tab was the last also,
        # to do certain actions when the user leaves a tab
        # start at the first tab in both these tabwidgets
        self.current_tab = 0
        self.current_table_tab = 0

        self.setCurrentIndex(self.current_tab)
        self.currentChanged.connect(self.mainTabChange)

        # open this separate dialog window when this is clicked
        self.SeparateWindow = SeparateWindow(self.window)

        # loads settings from data/settings.txt
        # if file does not exist, uses default settings
        # settings also contain a list of previously accessed database paths
        self.settings = Settings(self, SETTINGS_PATH)

        # load settings after the settings attribute has been created
        self.settings.load()

        # connect all actions to their UI elements
        self.setupAllTabs()

        self.window.setStatus('Nothing loaded', side='left')
        self.window.setStatus('No data', side='right')

    def mainTabChange(self, idx):
        """
        this method is called whenever the tab changes in the main app
        idx is the index of the current tab (i.e. the one that was changed to)
        """
        print(f'changed from tab {self.current_tab} → {idx}')

        if idx == self.indexOf(self.ui.LogTab):
            self.setupLogTab()

        self.current_tab = idx

    def setupAllTabs(self):
        """
        calls the setup method for all tabs in the correct order
        """

        self.setupMainTab()
        self.setupLogTab()

    def setupMainTab(self):

        self.ui.TestButton.clicked.connect(self.SeparateWindow.show)

        def long_func():

            with progress(self, 'Long process...') as pb:

                def cb(val):

                    pb.setValue(val)
                    pb.update()

                import time

                for n in range(100):

                    time.sleep(0.05)
                    cb(n)

        self.ui.ShowProgressButton.clicked.connect(long_func)

        def get_dir():

            directory = BrowseDialog().getDirectory()

            if directory:
                print(directory)

        self.ui.FolderSelectButton.clicked.connect(get_dir)

        def get_files():

            files = BrowseDialog().getMultipleFiles(filter_str='Text files (*.txt)')

            if files:
                print(files)

        self.ui.FilesSelectButton.clicked.connect(get_files)

    def setupLogTab(self):
        """
        sets up the log tab

        reloads each time the tab is accessed
        """

        textbrowser = self.ui.LogBrowser

        # log file is deleted on program startup, so it cannot become too long
        # so it's safe to just read this from scratch each time
        with open(LOG_PATH, 'r', encoding='utf-8') as f:

            lines = f.read().split('\n')

            rich_text = '<br>'.join([process_log_line(n) for n in lines])
            textbrowser.setText(rich_text)

        # ensure that the last line is visible
        textbrowser.verticalScrollBar().setValue(
            textbrowser.verticalScrollBar().maximum())

    def disableUI(self):
        """
        disables all UI elements

        all of these elements are re-enabled at the appropriate
        part of their associated methods
        """

        pass

    def displayTable(self, table, cols, vals):
        """
        populates a QTableWidget with a progress indicator
        """

        with progress(self, 'Displaying table...') as pb:

            def callback(x):
                pb.setValue(x)
                pb.update()

            callback(0)

            populate_table(table, cols, vals,
                           callback=callback)
