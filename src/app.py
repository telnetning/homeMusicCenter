#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import web
import db #初始化数据操作
import admin #后台管理界面子应用
import data #数据接口子应用
import store #存储操作子应用
import MySQLdb

urls = (
       '/admin', 'admin.admin_app',
       '/data', 'data.data_app',
       '/store', 'store.store_app',
        )

if __name__ == '__main__':
    try:
        db.initDb()
    except MySQLdb.Error:
        print "hello" 
