#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import MySQLdb
import json

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "password"
DB_PORT = 3306

#create databases and tables
def initDb():
    try:
        conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASS, port = DB_PORT)
    except MySQLdb.Error:
        print "Wrong init db: cann't connect to mysql."
    
    cur = conn.cursor();
    cur.execute("create database if not exists hmc") 
    cur.execute("use hmc")
    #cur.execute("create table a(jdoc json)")
    
    createSongs = '''create table if not exists songs(
                        id int not null auto_increment primary key,
                        name varchar(200) not null,
                        singer varchar(100),
                        album int default -1,
                        duration int not null,
                        cover varchar(150),
                        comment varchar(1000)
                     )'''
    createAlbums = '''create table if not exists albums(
                        id int not null auto_increment primary key,
                        name varchar(200),
                        published int,
                        cover varchar(150),
                        comment varchar(1000)
                      )'''
    createSingers = '''create table if not exists singer(
                        id int not null auto_increment primary key,
                        name varchar(100) not null
                       )'''
    createSongsLists = '''create table if not exists songsList(
                            id int not null auto_increment primary key,
                            name varchar(100),
                            comment varchar(1000),
                            songs json
                          )'''

    cur.execute(createSongs)
    cur.execute(createAlbums)
    cur.execute(createSingers)
    cur.execute(createSongsLists)

if __name__ == '__main__':
    initDb()
    pass
