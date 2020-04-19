from PyQt5 import QtCore, QtWidgets
from contextlib import contextmanager


class ProgressBarForm:

    def setupUi(self, Form):

        Form.setObjectName('Form')
        Form.resize(400, 90)

        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(30, 30, 340, 30))

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        sizePolicy.setHeightForWidth(
            self.progressBar.sizePolicy().hasHeightForWidth())

        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(340, 30))
        self.progressBar.setMaximumSize(QtCore.QSize(340, 30))

        self.progressBar.setProperty('value', 0)
        self.progressBar.setObjectName('progressBar')

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'Progress bar'))


class MyProgressBar(QtWidgets.QDialog, ProgressBarForm):

    def __init__(self, parent=None, description=None, busy=False):
        """
        a progressbar that prevents focus elsewhere in the GUI

        if busy=True, show a busy indication instead of progress
        """

        super(MyProgressBar, self).__init__(
            parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)

        self.setupUi(self)

        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.app = parent.app
        self.currval = 0

        self.show()

        if busy:
            self.progressBar.setMinimum(0)
            self.progressBar.setMaximum(0)
            self.setValue(0)

        if description is not None:
            self.setDescription(description)

    def setValue(self, val):

        self.progressBar.setProperty('value', val)
        self.currval = val

    def setDescription(self, description):
        self.setWindowTitle(description)

    def update(self):
        self.app.processEvents()


@contextmanager
def progress(parent, description='Progress', busy=False) -> MyProgressBar:
    """
    context manager for a progress bar

    yields the MyProgressBar instance that is created

    need to call pb.update() to update pb manually where this is used,
    for example each iteration in a loop
    """

    pb = MyProgressBar(parent, description=description, busy=busy)

    # make sure the progressbar starts at 0
    pb.setValue(0)
    pb.update()

    yield pb

    pb.close()
