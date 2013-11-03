#-*-coding:utf-8-*-

import requests
import json,time
from logbook import Logger
from Data import Data

class Share:
    __request_url = 'http://pan.baidu.com/pcloud/feed/getsharelist?t=%d&start=%d&limit=%d&category=0&auth_type=1&query_uk=%s'
    __request_count = 100
    __db = Data('share')

    def __init__(self,uk,offset):
        self.__request_offset = offset
        self.__request_uk = uk

    def __getJSONContent(self):
        ts = int(time.time())
        toRequest = Share.__request_url % (ts,self.__request_offset,Share.__request_count,self.__request_uk)
        r = requests.get(toRequest)
        if(r.status_code == 200):
            return json.loads(r.text)
        else:
            return None

    def __getShareCount(self):
        toRequest = Share.__request_url % (int(time.time()),0,1,self.__request_uk)
        r = requests.get(toRequest)
        if(r.status_code == 200):
            res = json.loads(r.text)
            return int(res['total_count'])
        else:
            return None

    def __save(self,content):
        for item in content:
            shareid = item['shareid']
            uk = item['uk']
            for file in item['filelist']:
                saveObj = {}
                saveObj['uk'] = uk
                saveObj['shareid'] = shareid
                saveObj['size'] = file['path']
                saveObj['md5'] = file['md5']
                if 'thumburl' in file:
                    saveObj['thumburl'] = file['thumburl']
                if 'dlink' in file:
                    saveObj['dlink'] = file['dlink']
                saveObj['fs_id'] = file['fs_id']
                saveObj['filename'] = file['server_filename']
                if Share.__db.exist('share',{'fs_id':saveObj['fs_id']}) == False:
                    Share.__db.save(saveObj)


    def spam(self):
        share_count = self.__getShareCount()
        if share_count!= None:
            while share_count > self.__request_offset:
                result = self.__getJSONContent()
                if result != None:
                    self.__save(result['records'])
                    self.__request_offset += Share.__request_count
                else:
                    continue

if __name__ == '__main__':
    share = Share(1647262388,0)
    share.spam()
