#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from db import DB
import sys
import os

if(len(sys.argv) != 2):
    raise Exception("Usage : %s filename.db" % sys.argv[0])

filename = sys.argv[1]

os.system("rm -f %s" % filename)

DB.open(filename)



DB.doUpdate("create TABLE counters (id integer primary key, name text)")
DB.doUpdate("create table recordings (id integer primary key, idcounter int, date text, value int)")

DB.close()
