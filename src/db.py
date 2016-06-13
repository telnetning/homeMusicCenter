#!/usr/bin/env python2
#-*- coding: utf-8 -*-
# 初始化数据库

import MySQLdb
from hmcException import ConnError, CreateError

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "password1"
DB_PORT = 3306

#create databases and tables
def initDb():
    try:
        conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASS, port = DB_PORT)
        cur = conn.cursor();
    except MySQLdb.Error:
        raise ConnError
        #print "Wrong init db: cann't connect to mysql."
    
    cur.execute("create database if not exists hmc") 
    cur.execute("use hmc")
    #cur.execute("create table a(jdoc json)")

    createSongs = '''create table songs(
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
    try:                       
        cur.execute(createSongs)
        cur.execute(createAlbums)
        cur.execute(createSingers)
        cur.execute(createSongsLists)
    except MySQLdb.Error:
        raise CreateError
