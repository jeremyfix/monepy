#!/usr/bin/env python3
# -*- coding: utf-8 *-*

from db import DB
from counter import Counter
from recording import Recording
import datetime
import os


DB.open('example.db')

#### Add some counters
elec = Counter("Electricité")
elec.insert()
print(elec)

gaz = Counter("Gaz")
gaz.insert()
print(gaz)

print("")

#### List all the counters
print("List all : ")
allcounters = Counter.findAll()
for c in allcounters:
    print(str(c))



#### Put some recordings
r = Recording(elec.id, datetime.datetime.strptime("2015-10-01", "%Y-%m-%d"), 1000)
r.insert()
r = Recording(elec.id, datetime.datetime.strptime("2015-10-05", "%Y-%m-%d"), 1500)
r.insert()


r = Recording(gaz.id, datetime.datetime.strptime("2015-10-01", "%Y-%m-%d"), 100)
r.insert()
r = Recording(gaz.id, datetime.datetime.strptime("2015-10-10", "%Y-%m-%d"), 200)
r.insert()

#### List all the counters
print("List all : ")
s = Recording.findAll()
for r in s:
    print(str(r))

for c in allcounters:
    print("All of : %s" % c.name)
    s = Recording.findByIdCounter(c.id)
    for r in s:
        print(str(r))






DB.close()
