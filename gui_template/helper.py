import qdarkstyle
from traceback import format_exc
import datetime

from PyQt5.QtWidgets import (QMessageBox,
                             QTableWidgetItem,
                             QListWidgetItem,
                             QLabel)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt

from gui_template.misc import is_null, convert_to_numeric
from gui_template.logger import logger


class SortableTableItem(QTableWidgetItem):

    def __init__(self, text, sortKey):
        QTableWidgetItem.__init__(self, text, QTableWidgetItem.UserType)
        self.text = text
        self.sortKey = sortKey

    def __lt__(self, other):

        # if both are numbers, compare the numbers
        if isinstance(self.sortKey, (float, int)) and isinstance(other.sortKey, (float, int)):
            return self.sortKey < other.sortKey

        # otherwise compare the actual values as str
        return self.text < other.text


def set_window_icon(app):

    icon = QIcon()
    icon.addFile('assets/app-icon.png', QSize(256, 256))

    app.setWindowIcon(icon)


def set_stylesheet(app):
    """
    sets a dark theme for all GUI elements (qdarkstyle)
    """
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


def set_valid_label(label: QLabel, valid=True, height=20) -> None:
    """
    sets label to a green/red checkmark icon
    """

    if valid:
        icon_name = 'valid-icon.png'

    else:
        icon_name = 'invalid-icon.png'

    # NOTE: hardcoded path
    icon = QPixmap(
        f'(gui_template\\ui\\../../assets/{icon_name}').scaledToHeight(height,
                                                                       Qt.SmoothTransformation)

    label.setPixmap(icon)


def show_error_message(text='', heading='Error', title='Error',
                       exception=False,
                       icon=QMessageBox.Critical):
    """
    show an error message dialog box, takes focus and has OK button

    logs the message with ERROR
    """

    if exception:
        exception_str = format_exc()
        text = f'{text}\n\n{exception_str}'

    msg = QMessageBox()
    msg.setIcon(icon)

    msg.setText(heading)
    msg.setInformativeText(text)
    msg.setWindowTitle(title)

    # the logger does not deal with multiline text
    for line in text.split('\n'):

        # need to call logger.error to get correct level
        logger.error(line)

    msg.exec_()


def show_info_message(text='', heading='Information', title='Information',
                      icon=QMessageBox.Information):
    """
    show an information message dialog box, takes focus and has OK button
    """

    msg = QMessageBox()
    msg.setIcon(icon)

    msg.setText(heading)
    msg.setInformativeText(text)
    msg.setWindowTitle(title)

    msg.exec_()


def show_yes_no_dialog(parent, title='', text='') -> bool:
    """
    shows a yes/no dialog box
    returns True for yes and False for no
    """

    response = QMessageBox.question(parent, title, text,
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)

    if response == QMessageBox.Yes:
        return True
    else:
        return False


def list_move_selected(list1, list2, sort1=False, sort2=False):
    """
    moves selected items from list1 → list2

    adds the selected item in list1 to end of list2
    and removes them from list1

    assumes that list1 and list2 do not contain duplicate elements
    """

    selected = list1.selectedItems()

    for item in selected:
        list2.addItem(item.text())
        list1.takeItem(list1.row(item))


def populate_list(widget, vals):

    # need to clear the existing items first
    widget.clear()

    for i, row in enumerate(vals):

        val = vals[i]

        item = QListWidgetItem(str(val))

        widget.insertItem(i, item)


def clear_table(table):
    """
    removes all rows and columns of table
    """

    # if the table was sorted by the user, and this is not done, the refresh is very slow
    table.setRowCount(0)
    table.setColumnCount(0)

    table.clear()


def populate_table(table, cols, vals, callback=None):
    """
    populates table with data in cols, vals

    converts numerical strings to numerical to make sorting word as expected
    table is a QTableWidget
    """

    N = len(vals)
    M = len(cols)

    clear_table(table)

    table.setRowCount(N)
    table.setColumnCount(M)

    for i, row in enumerate(vals):
        for j, col in enumerate(cols):

            val = vals[i][j]

            # if the value is a representation of null or empty str / just whitespace
            # display string [EMPTY] here, since it is needed in the update table at least
            if val != '[EMPTY]' and (is_null(val) or (isinstance(val, str) and not val.strip())):
                continue

            if isinstance(val, datetime.datetime):

                # format 17-03-20 18:44:15
                val_str = val.strftime('%d-%m-%Y %H:%M:%S')

                # use int timestamp for sorting
                val = val.timestamp()

            elif isinstance(val, datetime.timedelta):

                val_str = str(val)
                val = val.total_seconds()

            else:
                val = convert_to_numeric(val)
                val_str = str(val)

            # QTableWidgetItem only accepts string values
            # the default implementation only sorts according to string values
            # SortableTableItem displays the first value,
            # and uses the second one for sorting
            item = SortableTableItem(val_str, val)

            table.setItem(i, j, item)

        # callback for each row
        if callback:
            callback(100 * i / (N * 1.1))

    # set the column header names
    for j, col in enumerate(cols):

        if callback:
            callback(97 - 5 * (1 - (j / M)))

        item = QTableWidgetItem(col)
        table.setHorizontalHeaderItem(j, item)

    if callback:
        callback(98)
    table.resizeColumnsToContents()

    if callback:
        callback(99)

    table.resizeRowsToContents()

    if callback:
        callback(100)


def get_list_items(listwidget) -> list:
    return [listwidget.item(i).text() for i in range(listwidget.count())]
