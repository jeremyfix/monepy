# -*- coding: utf-8 *-*

from db import DB
from counter import Counter
import datetime


class Recording:

    def __init__(self, idcounter, date, value):
        assert(type(date) is datetime.datetime)
        self.id = None
        self.idcounter = idcounter
        self.date = date
        self.value = value

    def insert(self):
        query = "insert INTO recordings VALUES (NULL,%i,'%s',%i)" % (self.idcounter, self.date.strftime("%Y-%m-%d %H:%M:%S")+".000", self.value)
        id = DB.do_update(query)
        self.id = id


    def update(self):
        if self.id is not None:
            query = "update recordings SET value=%i where id=%i" % (self.value, self.id)
            DB.do_update(query)

    def remove(self):
        if self.id is not None:
            query = "delete from recordings where id=%i" % self.id
            res = DB.do_update(query)

    def __str__(self):
        return "Recording : Id %i; Counter : %s; Date : %s ; Value : %i" % (self.id, Counter.findById(self.idcounter).name, self.date.strftime("%Y-%m-%d %H:%M:%S"), self.value)
        
    @staticmethod
    def findAll():
        query = "select * from recordings"
        res = DB.do_select(query)
        allr = []
        for (id,idcounter, date, value) in res:
            # the date is recorded as a string with trailing millisecondes; see insert()
            d = datetime.datetime.strptime(date[:-4], "%Y-%m-%d %H:%M:%S")
            r = Recording(idcounter, d, value)
            r.id = id
            allr.append(r)
        return allr

    @staticmethod
    def findByIdCounter(idcounter):
        query = "select * from recordings where idcounter=%i" % idcounter
        res = DB.do_select(query)
        allr = []
        for (id,idcounter, date, value) in res:
            d = datetime.datetime.strptime(date[:-4], "%Y-%m-%d %H:%M:%S")
            r = Recording(idcounter, d, value)
            r.id = id
            allr.append(r)
        return allr

    @staticmethod
    def findById(id):
        query = "select * from recordings where id=%i" % id
        res = DB.do_select(query)
        allr = []
        if(len(res) != 1):
            raise Exception("Not enough or too many results !!")


        (id,idcounter, date, value) = res[0]
        d = datetime.datetime.strptime(date[:-4], "%Y-%m-%d %H:%M:%S")
        r = Recording(idcounter, d, value)
        r.id = id
        return r

