import os
import re

import settings


from PyQt5.QtCore import (
    QDir, QRunnable, pyqtSlot, pyqtSignal, QObject)

from PyQt5.QtWidgets import (
    QFileDialog, QDialog, QHeaderView,
    QTableWidgetItem, QMessageBox, QMenu,
    QAction
)


def convertFileSize(size_bytes):
    import math

    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def timeHandler(timeSec=0, unit="", strDate="", readable=False, getCurrentTime=False):
    import datetime as dt

    if unit == "s":
        seconds = timeSec
        minutes = seconds // 60
        seconds = seconds % 60
        newTime = {"min": minutes, "sec": seconds}
        return newTime

    if unit == "ms":
        seconds = timeSec / 1000
        minutes = seconds // 60
        newTime = {"min": minutes, "sec": seconds}
        return newTime

    if strDate != "" and readable:
        newTime = f"{dt.datetime.strptime(strDate, '%Y-%m-%d %H:%M:%S'):%b %d %Y %H:%M.%S %p}"
        return newTime

    if getCurrentTime:

        if readable:
            currentTime = f"{dt.datetime.now():%b %d %Y %H:%M.%S %p}"
        else:
            currentTime = dt.datetime.now()

        return currentTime


def fileDialog(directory='', forOpen=True, fmt='', isFolder=False):
    options = QFileDialog.Options()

    options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.DontUseCustomDirectoryIcons
    dialog = QFileDialog()
    dialog.setOptions(options)

    dialog.setFilter(dialog.filter() | QDir.Hidden)

    if isFolder:
        dialog.setFileMode(QFileDialog.DirectoryOnly)
    else:
        dialog.setFileMode(QFileDialog.AnyFile)

    dialog.setAcceptMode(QFileDialog.AcceptOpen) if forOpen else dialog.setAcceptMode(QFileDialog.AcceptSave)

    if fmt != '' and isFolder is False:
        dialog.setDefaultSuffix(fmt)
        dialog.setNameFilters([f'{fmt} (*.{fmt})'])

    if directory != '':
        dialog.setDirectory(str(directory))
    else:
        dialog.setDirectory(str(settings.ROOT_DIR))

    if dialog.exec_() == QDialog.Accepted:
        path = dialog.selectedFiles()[0]
        return path
    else:
        return ''


def loadUiFile(classUI, fileName):
    from PyQt5 import uic
    uiFile = uic.loadUi(os.path.join(settings.UI_DIR, fileName), classUI)
    return uiFile


def loadCsvToTable(csv_file, tableWidget):
    import pandas as pd

    df = pd.read_csv(csv_file)
    print(df)

    nRows, nColumns = df.shape
    tableWidget.setRowCount(nRows)
    tableWidget.setColumnCount(nColumns)
    tableWidget.setHorizontalHeaderLabels(list(df.columns.values))
    tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    for i in range(tableWidget.rowCount()):
        for j in range(tableWidget.columnCount()):
            tableWidget.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))


def generateId(id_type):
    import uuid
    import random
    import string

    if id_type == 'uuid':
        return str(uuid.uuid4())

    elif id_type == 'string':
        str1 = "".join((random.choice(string.ascii_letters) for _ in range(5)))
        str1 += "".join((random.choice(string.digits) for _ in range(5)))
        sam_list = list(str1)
        random.shuffle(sam_list)
        random_id = "".join(sam_list)
        return random_id

    elif id_type == 'number':
        return random.randint(1, 100000)
    else:
        return None


def show_message(text: str, class_ui, message_type="information"):
    if message_type == 'information':
        QMessageBox.information(class_ui, 'Message', text)

    elif message_type == 'question':
        reply = QMessageBox.question(
            class_ui, 'Message', text,
            QMessageBox.Yes, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            return True
        else:
            return False


def filter_string(text: str, phone=False, email_address=False, return_list=False):
    if phone:
        pattern = r'\b(?:\+1\s?)?(?:\d{10}|\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\(\d{3}\)\s?\d{3}[-.\s]?\d{4}|\d{7})\b'
        matches = re.findall(pattern, text)

        numbers_ = []
        for match in matches:
            cleaned_number = re.sub(r'\D', '', match)
            formatted_number = re.sub(r'(\d{3})(\d{3})(\d{4})', r'\1-\2-\3', cleaned_number)
            numbers_.append(formatted_number)

        if return_list:
            return numbers_
        else:
            return numbers_[0]

    elif email_address:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        emails = re.findall(email_pattern, text)
        if return_list:
            return emails
        else:
            return emails[0]

    else:
        return


def load_items_to_tree(csv_file, tableWidget):
    import pandas as pd

    df = pd.read_csv(csv_file)
    print(df)

    nRows, nColumns = df.shape
    tableWidget.setRowCount(nRows)
    tableWidget.setColumnCount(nColumns)
    tableWidget.setHorizontalHeaderLabels(list(df.columns.values))
    tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    for i in range(tableWidget.rowCount()):
        for j in range(tableWidget.columnCount()):
            tableWidget.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))


class Signals(QObject):
    finished = pyqtSignal(object)


class Worker(QRunnable):

    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signal = Signals()

    @pyqtSlot()
    def run(self):
        result = self.function(*self.args, **self.kwargs)
        self.signal.finished.emit(result)

