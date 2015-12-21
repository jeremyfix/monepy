# -*- coding: utf-8 *-*

from db import DB


class Counter:

    def __init__(self, name):
        self.id = None
        self.name = name

    def insert(self):
        query = "insert INTO counters VALUES (NULL,'%s')" % self.name
        id = DB.do_update(query)
        self.id = id
        

    def __str__(self):
        return "Counter : Id %i - Name %s" % (self.id, self.name)
        
    @staticmethod
    def findAll():
        query = "select * from counters"
        res = DB.do_select(query)
        allc = []
        for (id,name) in res:
            c = Counter(name)
            c.id = id
            allc.append(c)
        return allc

    @staticmethod
    def findById(id):
        query = "select * from counters where id=%i" % id
        res = DB.do_select(query)
        if len(res) != 1:
            raise Exception("Issue while requesting counter id=%i ; got %i results" % (id, len(res)))
        
        c = Counter(res[0][1])
        c.id = res[0][0]
        return c
