import sys

import matplotlib
matplotlib.use('Qt4Agg')
import pylab

import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates

from PyQt4 import Qt
from PyQt4 import QtCore
# from PyQt4.QtCore import SIGNAL, SLOT, pyqtSlot
from functools import partial
# import PyQt4.Qwt5 as Qwt
# from PyQt4.Qwt5.anynumpy import *
from PyQt4.QtGui import QDialog, QWidget, QGridLayout, QTableWidget,QTableWidgetItem,  QStyleFactory, QMainWindow, QFrame, QTabWidget, QHBoxLayout, QAction, QIcon, qApp, QPushButton
from PyQt4.QtCore import QSize

import calendar
# import datetime
# import os


from db import DB
from counter import Counter
from recording import Recording
from registerDialog import RegisterDialog


class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        # The tabs, one per counter
        self.tabs = QTabWidget()
        #self.tabs.currentChanged.connect(self.currentTabChanged)
        #self.current_tab = 0
        self.setupTabs()

        self.setCentralWidget(self.tabs)

        self.statusBar()
        
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        registerAction = QAction('Register', self)
        registerAction.setShortcut('Ctrl+R')
        registerAction.setStatusTip('Register new counter entry')
        registerAction.triggered.connect(self.register)


        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")

        fileMenu.addAction(registerAction)
        fileMenu.addAction(exitAction)

    def setupTabs(self):
        #self.tabs.currentChanged.disconnect(self.currentTabChanged)
        while(self.tabs.count() > 0):
            self.tabs.removeTab(0)

        self.tables = {}
        allcounters = Counter.findAll()
        for c in allcounters:
            tab = QWidget(self.tabs)
            hl = QHBoxLayout()
            tab.setLayout(hl)
            
            recordings = Recording.findByIdCounter(c.id)

            tw = QTableWidget(len(recordings), 5)
            self.tables["%i"%c.id] = tw
            column_names = QtCore.QStringList(["Id","Counter", "Date", "Value", "Remove ?"])
            tw.setHorizontalHeaderLabels(column_names)

            # Fill the table with the recordings
            for i, r in enumerate(recordings):
                # The id of the recording in the table of recordings
                item = QTableWidgetItem(QtCore.QString.number(r.id))
                item.setFlags(QtCore.Qt.NoItemFlags)
                tw.setItem (i, 0, item)
                
                # The id of the associated counter
                item = QTableWidgetItem(QtCore.QString.number(r.idcounter))
                item.setFlags(QtCore.Qt.NoItemFlags)
                tw.setItem (i, 1, item)

                # The date when the recording has been made
                item = QTableWidgetItem(QtCore.QString(r.date.strftime("%Y-%m-%d %H:%M:%S")))
                item.setFlags(QtCore.Qt.NoItemFlags)
                tw.setItem (i, 2, item)

                # The value can be edited
                item = QTableWidgetItem(QtCore.QString.number(r.value))
                item.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)

                tw.setItem (i, 3, item)

                but = QPushButton("Remove")
                but.clicked.connect(partial(self.on_removeClicked, counter_id=c.id, recording_id=r.id))
                #item = QTableWidgetItem(but)
                #tw.setItem(i, 4, but)
                #tw.setIndexWidget()
                tw.setCellWidget(i, 4, but)

            tw.cellChanged.connect(partial(self.on_cellChanged, counter_id=c.id))

            # We allow sorting and we sort by decreasing date
            # to get the most recent recordings at the top
            tw.setSortingEnabled(True)
            tw.sortByColumn(2, QtCore.Qt.DescendingOrder)

            # Ajust the width of the columns to better see the contents
            tw.resizeColumnsToContents()
            tw.setFixedWidth(600)
            hl.addWidget(tw)

            #### Plot the data
            canvas = self.plot_data(recordings)
            hl.addWidget(canvas)


            self.tabs.addTab(tab,str(c.id) + "-" + c.name)   

        #self.tabs.setCurrentIndex(self.current_tab)

    #def currentTabChanged(self, tab_index):
    #    self.current_tab = tab_index

    def on_cellChanged(self, i, j, counter_id):
        tw = self.tables["%i"%counter_id]
        recordingId = int(tw.item(i,0).text())
        r = Recording.findById(recordingId)
        r.value = int(tw.item(i,3).text())
        r.update()
        self.setupTabs()


    def on_removeClicked(self, counter_id, recording_id):
        r = Recording.findById(recording_id)
        r.remove()
        self.setupTabs()

    def register(self):
        dialog = RegisterDialog(self)
        dialog.setVisible(True)
        dialog.show()
        dialog.closed.connect(self.setupTabs)

    def plot_data(self, recordings):
        fig = Figure(figsize=(200,200), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        ax = fig.add_subplot(111)

        # Sort the recordings by increasing date
        recordings = sorted(recordings, key=lambda r: r.date)

        # list of tuples (year, month, day, consumption, index)
        interpolated_consumptions = []

        for r in recordings:
            if(len(interpolated_consumptions) == 0):
                year = r.date.year
                month = r.date.month
                day = r.date.day
                cons = 0
                index = r.value
                interpolated_consumptions.append((year, month, day, cons, index))
                continue

            prev_entry = interpolated_consumptions[-1]
            prev_year, prev_month, prev_day, prev_cons, prev_index = prev_entry
            cur_year, cur_month, cur_day, cur_index = r.date.year, r.date.month, r.date.day, r.value

            # Necessarily, as we sorted the data, we have :
            # prev_year <= cur_year and prev_month <= cur_month


            # Point : determine r.cons and fill in between with intermediate consumptions
            #         to get one entry per month in interpolated_consumptions

            if prev_year == cur_year and prev_month == cur_month:
                # We can guarantee that we have consumed cur_index - prev_index
                # on this month;
                interpolated_consumptions[-1] = (cur_year, cur_month, cur_day, prev_cons + (cur_index - prev_index), cur_index)
            elif prev_year == cur_year:
                # and prev_month != cur_month
                #print("Last entry : %i - %i - %i" % (prev_year, prev_month, prev_day))
                tot_cons = cur_index - prev_index
                tot_days = 0
                nb_days = []
                # For the first month
                nb_days.append((prev_year, prev_month, nb_days_in_month(prev_year, prev_month) - prev_day))
                tot_days += nb_days_in_month(prev_year, prev_month) - prev_day
                # For the months in between
                for m in range(prev_month+1, cur_month):
                    days = nb_days_in_month(prev_year, m)
                    nb_days.append((prev_year, m, days))
                    tot_days += days
                # For the last month
                tot_days += cur_day
                nb_days.append((prev_year, cur_month, cur_day))
                #print(nb_days)
                #print(" A total of %i days" % tot_days)

                # We can now provide the interpolated values for interpolated_consumptions
                # The last entry has to be modified to close the month
                interpolated_consumptions[-1] = (prev_year, prev_month, nb_days_in_month(prev_year, prev_month), prev_cons + float(nb_days[0][2])/tot_days * tot_cons, -1)
                for (yr, mth, nbd) in nb_days[1:-1]:
                    interpolated_consumptions.append((yr, mth, nb_days_in_month(yr, mth), float(nbd) / tot_days * tot_cons, -1))
                # For the last month, we need to take the correct day..
                (yr, mth, nbd) = nb_days[-1]
                interpolated_consumptions.append((yr, mth, cur_day, float(nbd) / tot_days * tot_cons, cur_index))
            else:
                # we are not in the same year
                tot_cons = cur_index - prev_index
                tot_days = 0
                nb_days = []
                #####
                ## Deal with the consummption until the end of the year
                # For the first month
                nb_days.append((prev_year, prev_month, nb_days_in_month(prev_year, prev_month) - prev_day))
                tot_days += nb_days_in_month(prev_year, prev_month) - prev_day
                for m in range(prev_month, 13):
                    nb_days.append((prev_year, m, nb_days_in_month(prev_year, m)))
                    tot_days += nb_days_in_month(prev_year, m)

                # Deal with the years in between
                for yr in range(prev_year+1, cur_year):
                    for m in range(1, 13):
                        nb_days.append((yr, m, nb_days_in_month(yr, m)))
                        tot_days += nb_days_in_month(yr, m)

                # Deal with the months until the current month and year
                for m in range(1, cur_month):
                    nb_days.append((cur_year, m, nb_days_in_month(cur_year, m)))
                    tot_days += nb_days_in_month(cur_year, m)
                # Deal with the last month
                nb_days.append((cur_year, cur_month, cur_day))
                tot_days +=  cur_day

                interpolated_consumptions[-1] = (prev_year, prev_month, nb_days_in_month(prev_year, prev_month), prev_cons + float(nb_days[0][2])/tot_days * tot_cons, -1)
                for (yr, mth, nbd) in nb_days[1:-1]:
                    interpolated_consumptions.append((yr, mth, nb_days_in_month(yr, mth), float(nbd) / tot_days * tot_cons, -1))
                # For the last month, we need to take the correct day..
                (yr, mth, nbd) = nb_days[-1]
                interpolated_consumptions.append((yr, mth, cur_day, float(nbd) / tot_days * tot_cons, cur_index))


        # We now have the interpolated_consumptions
        # We split them by year ;
        years = []
        for yr,mth,day,cons,index in interpolated_consumptions:
            if yr not in years:
                years.append(yr)

        nyears = len(years)
        data = np.zeros((len(years),12))
        data.fill(np.nan)
        for yr, mth, day, cons, index in interpolated_consumptions:
            data[years.index(yr), mth-1] = cons


        ax.plot(range(1,13), data.T)
        ax.set_xlim([1,12])
        ylim = ax.get_ylim()
        ax.set_ylim([0, ylim[1]])
        ax.legend(years, loc='upper center')

        ax.set_xticks(range(1,13))
        ax.set_xticklabels( ['Jan.','Feb.','March', 'April', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'], rotation=45 )
        ax.set_ylabel('Delta index')

        #fig.autofmt_xdate()
        #ax.fmt_xdata = mdates.DateFormatter('%m')

        # generate the canvas to display the plot
        canvas = FigureCanvas(fig)
        canvas.setFixedSize(QSize(600,400))
        return canvas

def nb_days_in_month(year, month):
    r = calendar.monthrange(year, month)
    return r[1]

def main(args):
    DB.open('data.db')


    app = Qt.QApplication(args)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())  


if __name__ == '__main__':
    main(sys.argv)
