# monepy
Monitor your energy consumption in Python

This is a simple GUI to record and plot the evolution of your energy consumption; To use it , simply call :

python scripts/main_app.py

This is written in Python and only makes use of local files, without requiring to start any web interface as other projects would do (e.g. emoncms). Indeed, the indexes of your counters are stored in a sqlite file that you fill and modify from the GUI and then the consumption is computed and plotted individually for each counter, each year, month by month. 

As an example, with two counters, it looks like this :


![Monepy screenshot](https://github.com/jeremyfix/monepy/raw/master/screenshot.png "Monepy Screenshot")

This is not yet compatible with Python3, at least because the interface of PyQt4 changed (QStringList unavailable)




