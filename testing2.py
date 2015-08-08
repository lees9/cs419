#!/usr/bin/python
# -*- coding: utf-8 -*-

## this just displays the select statement (making sure it works)


import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'password1', 'test');

with con: 

    cur = con.cursor()
    cur.execute("SELECT * FROM StarWars")

    rows = cur.fetchall()

    for row in rows:
        print row