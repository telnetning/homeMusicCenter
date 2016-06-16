#coding:utf-8
import id3reader
import os

class ParseSong():

    info = {"name":"", "singer":"", "album":""}
    
    def getInfo(self, songPath):
        self.useId3reader(songPath)
        self.useNeteasyReader(songPath) 
        return self.info

    #直接读 mp3 文件获取信息，不一定能获取到
    def useId3reader(self, songPath):
        id3r = id3reader.Reader(songPath)
        print self.info
        if id3r.getValue("title"):
            self.info["name"] = id3r.getValue("title")
        if id3r.getValue("performer"):
            self.info["singer"] = id3r.getValue("performer")
        if id3r.getValue("album"):
            self.info["album"] = id3r.getValue("album")
    
    #使用网易云音乐的歌曲命名格式来对歌曲基本信息进行解析
    def useNeteasyReader(self, songPath):
        '''来源为网易的音乐的格式
           {歌手1 歌手2……}[空格]-[空格]{歌名}[-{进一步的歌名说明}].mp3
        '''
        song = os.path.basename(songPath)
        splitList = song.split('-', 1) 
        
        if len(splitList) == 1:
            print "文件不符合网易云音乐歌曲命名规则"
            return 
        else:
            self.info["singer"] = splitList[0].strip()
            self.info["name"] = splitList[1][0:-4].strip()
