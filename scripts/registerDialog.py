from PyQt4.QtGui import QDialog, QGridLayout, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QComboBox, QLineEdit, QCalendarWidget
from PyQt4.QtCore import QSize, QDate, pyqtSignal
from PyQt4.Qt import Qt
import datetime

from counter import Counter
from recording import Recording

class RegisterDialog(QDialog):

    closed = pyqtSignal()

    def __init__(self, parent):
        super(RegisterDialog, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Registe a new counter entry")
        vbox = QVBoxLayout()

        # Setting up the widgets for selecting the counter
        hbox1 = QHBoxLayout()
        label = QLabel("Select the counter")
        hbox1.addWidget(label)

        self.comboCounter = QComboBox()
        self.comboCounter.addItem("None")
        allcounters = Counter.findAll()
        for c in allcounters:
            self.comboCounter.addItem(c.name)
        hbox1.addWidget(self.comboCounter)

        vbox.addLayout(hbox1)

        # Setting up the widgets for providing the value

        hbox2 = QHBoxLayout()
        label = QLabel("Value")
        hbox2.addWidget(label)

        self.lEdit = QLineEdit()
        hbox2.addWidget(self.lEdit)

        vbox.addLayout(hbox2)

        # Setting up the widgets to provide the date
        hbox3 = QHBoxLayout()
        label = QLabel("Date")
        hbox3.addWidget(label)

        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.on_cal_clicked)
        hbox3.addWidget(self.calendar)

        vbox.addLayout(hbox3)

        # Adding the push buttons to validate the entry of cancel it
        hbox4 = QHBoxLayout()
        okbutton = QPushButton("Ok")
        okbutton.clicked.connect(self.on_validate)

        hbox4.addWidget(okbutton)

        cancelbutton = QPushButton("Cancel")
        cancelbutton.clicked.connect(self.close)
        hbox4.addWidget(cancelbutton)


        vbox.addLayout(hbox4)


        self.setLayout(vbox)
        self.resize(QSize(100,100))

        now = datetime.datetime.now()
        self.current_date = datetime.datetime(now.year, now.month, now.day, 12)

    def on_cal_clicked(self, date):
        self.current_date =  datetime.datetime(date.year(), date.month(), date.day(), 12)

    def on_validate(self):
        idx_counter = self.comboCounter.currentIndex()
        value_counter = int(self.lEdit.text())

        if idx_counter == 0 or value_counter == "":
            self.close()
            return

        allcounters = Counter.findAll()
        counter = allcounters[idx_counter-1]

        r = Recording(counter.id, self.current_date, value_counter)
        r.insert()

        self.closed.emit()
        self.close()

