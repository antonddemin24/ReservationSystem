import calendar
from datetime import datetime

import sqlite3
import make_reservation
import delete_reservation
import show_all

from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtCore import QDate, QRectF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMessageBox, QCalendarWidget, QFormLayout, QLineEdit, \
    QHBoxLayout, QRadioButton, QLabel, QTabWidget, QPushButton
import sys

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QCalendarWidget, QApplication


def print_hi():
    connection = sqlite3.connect('reservation.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Reservation
                  (ID INT, Room TEXT, Date_in INT, Date_out INT, CustomerNro INT)''')
    connection.commit()
    connection.close()



class main_window(QTabWidget):

    def __init__(self, parent=None):
        super(main_window, self).__init__(parent)
        self.setGeometry(0, 0, 1000, 500)
        self.login()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.addTab(self.tab1, "Reservation")
        self.addTab(self.tab2, "Cancel reservation")
        self.combo = combodemo()
        self.tab1UI()
        self.tab2UI()
        self.setWindowTitle("Reservation system")

    def login(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Input Dialog',
                                        'Enter customer number:')
        if ok:
            self.cust_num = text


    def tab1UI(self):
        layout = QHBoxLayout()
        sec_layout = QtWidgets.QFormLayout()
        self.cal = CalendarDemo()
        self.cal.room = self.combo.selectionchange()
        layout.addWidget(self.cal)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.combo)
        sec_layout.addRow("Booked dates", layout)
        self.textbox2 = QLineEdit(self)
        self.textbox3 = QLineEdit(self)
        self.button = QPushButton('Run', self)
        self.button2 = QPushButton('Update', self)
        sec_layout.addRow(self.button2)
        sec_layout.addRow("Room", layout1)
        sec_layout.addRow("Date in", self.textbox2)
        sec_layout.addRow("Date out", self.textbox3)
        sec_layout.addRow(self.button)
        self.setTabText(0, "Reservation")
        self.tab1.setLayout(sec_layout)
        self.button.clicked.connect(self.onButtonClicked)
        self.button2.clicked.connect(self.update_button1)

    def onButtonClicked(self):
        if make_reservation.make_reserv(self.textbox2.text(), self.textbox3.text(), self.combo.selectionchange(), self.cust_num) is True:
            self.showdialog_done()
        else:
            self.showdialog_undone()
        self.update_button()

    def showdialog_done(self):
        msg = QMessageBox()
        msg.setWindowTitle("Reservation")
        msg.setText("Done!")
        msg.setIcon(QMessageBox.Warning)

        msg.exec_()

    def showdialog_undone(self):
        msg = QMessageBox()
        msg.setWindowTitle("Reservation")
        msg.setText("The room is already booked for the selected dates")
        msg.setIcon(QMessageBox.Warning)

        msg.exec_()

    def tab2UI(self):
        table = QtWidgets.QTableView()
        connection = sqlite3.connect('reservation.db')
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM Reservation WHERE CustomerNro =?""", (self.cust_num, ))
        result_set = cursor.fetchall()
        model = TableModel(result_set)
        table.setModel(model)
        layout = QHBoxLayout()
        layout.addWidget(table)
        sec_layout = QtWidgets.QFormLayout()
        sec_layout.addRow(layout)
        self.textbox4 = QLineEdit(self)
        button1 = QPushButton('Delete', self)
        sec_layout.addRow("Id", self.textbox4)
        sec_layout.addRow(button1)
        self.tab2.setLayout(sec_layout)
        button1.clicked.connect(self.onButtonClicked_2)

    def onButtonClicked_2(self):
        if delete_reservation.delete_reservation(self.textbox4.text()) is True:
            self.showdialog_done()
        else:
            self.showdialog_undone()
        self.update_button()

    def update_button(self):
        self.tab2.deleteLater()
        self.tab2 = QWidget()
        self.addTab(self.tab2, "Cancel reservation")
        self.tab2UI()

    def update_button1(self):
        self.tab1.deleteLater()
        self.tab1 = QWidget()
        self.addTab(self.tab1, "Reservation")
        self.tab1UI()


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def retutn_room(self):
        return self.combo.selectionchange()


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data




    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if self._data:
            return len(self._data[0])
        else:
            return 0


class CalendarDemo(QCalendarWidget):
    global currentYear, currentMonth

    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.move(0, 0)
        self.setGeometry(300, 300, 1000, 500)
        self.setGridVisible(True)
        self.setSelectionMode(0)

        self.setMinimumDate(QDate(currentYear, currentMonth - 1, 1))
        self.setMaximumDate(
            QDate(currentYear, currentMonth + 1, calendar.monthrange(currentYear, currentMonth)[1]))
        self.setSelectedDate(QDate(currentYear, currentMonth, 1))

        self.clicked.connect(self.printDateInfo)

    def paintCell(self, painter, rect, date):
        painter.setRenderHint(QPainter.Antialiasing, True)
        connection = sqlite3.connect('reservation.db')
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM Reservation WHERE Room = ?""", (self.room, ))
        result_set = cursor.fetchall()
        for row in result_set:
            lst = row[2].split(',')
            date1 = QDate(int(lst[0]), int(lst[1]), int(lst[2]))
            lst = row[3].split(',')
            date2 = QDate(int(lst[0]), int(lst[1]), int(lst[2]))
            while date1 != date2.addDays(1):
                if date == date1:
                    painter.drawRect(rect)
                    painter.save()
                    painter.setBrush(Qt.red)
                    painter.drawText(QRectF(rect), Qt.TextSingleLine | Qt.AlignCenter, str(date.day()))
                    painter.restore()
                else:
                    QCalendarWidget.paintCell(self, painter, rect, date)
                date1 = date1.addDays(1)
        QCalendarWidget.paintCell(self, painter, rect, date)

    def printDateInfo(self, qDate):
        print('{0},{1},{2}'.format(qDate.year(), qDate.month(), qDate.day()))
        print(f'Day Number of the year: {qDate.dayOfYear()}')
        print(f'Day Number of the week: {qDate.dayOfWeek()}')

    # def new_room(self):
    #     # self.deleteLater()
    #     # self.initUI()
    #     self.paintCell(self, )


class combodemo(QWidget):
    def __init__(self, parent=None):
        super(combodemo, self).__init__(parent)

        layout = QHBoxLayout()
        self.cb = QtWidgets.QComboBox()
        self.cb.addItems(["1", "2", "3", "4", "5", "6", "7", "8"])
        self.cb.currentIndexChanged.connect(self.selectionchange)


        layout.addWidget(self.cb)
        self.setLayout(layout)

    def selectionchange(self):
        print(self.cb.currentText())
        # CalendarDemo().new_room
        return self.cb.currentText()



if __name__ == '__main__':
    print_hi()
    app = QApplication(sys.argv)
    ex = main_window()
    ex.show()
    sys.exit(app.exec_())
