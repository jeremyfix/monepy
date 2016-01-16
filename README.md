# Monitor your energy consumption in Python

This is a simple GUI to record and plot the evolution of your energy consumption; To use it , simply call :

```
cd scripts
python main_app.py
```

Requirements : sqlite3, PyQt4 and matplotlib.


This is written in Python and only makes use of local files, without requiring to start any web interface as other projects would do (e.g. emoncms). Indeed, the indexes of your counters are stored in a sqlite file that you fill and modify from the GUI and then the consumption is computed and plotted individually for each counter, each year, month by month. 

As an example, with two counters, it looks like this :


![Monepy screenshot](https://github.com/jeremyfix/monepy/raw/master/screenshot.png "Monepy Screenshot")

This is not yet compatible with Python3, at least because the interface of PyQt4 changed (QStringList unavailable)

This is also not yet out of the box ; I created the database with setup_db.py ; Actually, there is not yet anything in the GUI to add a new counter; The GUI however is generic in the sense that it displays as many tabs as there are declared counters in the database. 


