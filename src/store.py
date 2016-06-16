#!/usr/bin/env python2
#coding=utf-8

# 定义各种向目录中添加数据的操作

import id3reader
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import time
from parseSong import ParseSong
from hmcException import *
import warnings
from db import Storage
import os

class HandlerSongOpe(FileSystemEventHandler):
    def __init__(self, hmcRoot):
        self.hmcRoot = hmcRoot

    def on_created(self, event):
        parser = ParseSong()
        info = parser.getInfo(event.src_path)

        if not info["name"]:
            warnings.warn("歌曲的命令格式不符合定义:" + event.src_path)
            return  
        
        db = Storage()
        cur = db.db
        
        if info["album"]:
            #albumQ = cur.select('album', 'select id from album where name=$name', vars={'name': info["name"]})
            albumQ = cur.select('albums', {'name': info['album']}, where = 'name=$name')
            if albumQ:
                albumNo = albumQ[0]["id"] 
            else:
                albumNo = cur.insert('albums', name = info["album"])

        if info["singer"]:
            #singerQ = cur.select('singer', "select id from singer wbere name=$name", vars= {'name': info['singer']})
            singerQ = cur.select('singers', {'name': info["singer"]}, where = 'name=$name')
            if singerQ:
                singerNo = singerQ[0]["id"]
            else:
                singerNo = cur.insert("singers", name = info["singer"])
        
        #建立歌曲文件的快捷方式用于 web 访问，快捷方式位于 {hmcRoot}/resources/song 下
        songName = os.path.basename(event.src_path)
        command = 'ln -s "' + event.src_path + '" ' + '"' + self.hmcRoot + '/resources/song/' + songName + '"'
        os.popen(command)
        #os.symlink('"' + self.hmcRoot + '/resource/song/' + songName + '"', '"' + event.src_path + '"')
        cur.insert('songs', name = info["name"], singer = singerNo, album = albumNo, path = event.src_path)

class main():
    songStroageDir = "."
    def __init__(self):
        stream = file('config.yml', 'r')
        config = yaml.load(stream)
        self.songStroageDir = config["songStroageDir"]
        self.hmcRoot = config["hmcRoot"] 

    def start(self):
        handler1 = HandlerSongOpe(self.hmcRoot)
        observer = Observer()
        try:
            watch = observer.schedule(handler1, path=self.songStroageDir, recursive=True)
        except OSError, e:
            raise e

        observer.start()

        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()
