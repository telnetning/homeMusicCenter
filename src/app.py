#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import web
import db #初始化数据操作
import admin #后台管理界面子应用
import data #数据接口子应用
#import store #存储操作子应用
from store import main
import MySQLdb
import thread
import time
from hmcException import *

urls = (
       '/admin', 'admin.admin_app',
       '/data', 'data.data_app',
       '/store', 'store.store_app',
        )

# 多线程的函数，用来启动 watchdog，监控目录中的文件变化
def watch():
    mm = main()
    print mm.songStroageDir
    mm.start()

if __name__ == '__main__':
    try:
        db.initDb()
    except CreateTableError:
        print "myslq operate has exception" 
    
    thread.start_new_thread(watch, ()) 
    
    app = web.application()
    app.run()
