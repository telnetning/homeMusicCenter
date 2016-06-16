#!/usr/bin/env python2
#-*- coding: utf-8 -*-
# 初始化数据库

import MySQLdb
from hmcException import ConnSqlError, CreateTableError
import web
import os

DB_HOST = os.getenv('HMC_MYSQL_HOST') 
DB_USER = os.getenv('HMC_MYSQL_USER') 
DB_PASS = os.getenv('HMC_MYSQL_PASS')
DB_PORT = int(os.getenv('HMC_MYSQL_PORT')) 

class Storage:
    def __init__(self):
        self.db = web.database(dbn = "mysql", db = "hmc", user = "root", pw="password")    
    
#create databases and tables
def initDb():
    try:
        conn = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASS, port = DB_PORT)
        cur = conn.cursor();
    except MySQLdb.Error:
        raise ConnSqlError
        #print "Wrong init db: cann't connect to mysql."
    
    cur.execute("create database if not exists hmc") 
    cur.execute("use hmc")
    #cur.execute("create table a(jdoc json)")

    createSongs = '''create table if not exists songs(
                        id int not null auto_increment primary key,
                        name varchar(200) not null,
                        singer int default -1,
                        album int default -1,
                        path varchar(500) not null default "fake path",
                        duration int,
                        cover varchar(150),
                        comment varchar(1000)
                     )'''
    createAlbums = '''create table if not exists albums(
                        id int not null auto_increment primary key,
                        name varchar(200) not null default "fake name",
                        singer int,
                        published int,
                        cover varchar(150),
                        comment varchar(1000)
                      )'''
    createSingers = '''create table if not exists singers(
                        id int not null auto_increment primary key,
                        name varchar(100) not null default "fake name"
                       )'''
    createSongsLists = '''create table if not exists songsLists(
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
    except MySQLdb.Error, e:
        raise CreateTableError
