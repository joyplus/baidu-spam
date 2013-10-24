#-*-coding:utf-8-*-

import requests
from logbook import Logger
from Data import Data
import json,time

class User:
    __request_url = 'http://pan.baidu.com/pcloud/friend/getfollowlist?query_uk=%d&limit=%d&start=%d'
    __request_count = 20;
    __db = Data('user')

    def __init__(self):
        self.__request_offset = 0
        self.__followCount = 20;

    def __getJSONContent(self,uk,start):
        toRequest = User.__request_url % (uk,User.__request_count,start)
        r = requests.get(toRequest)
        if(r.status_code == 200):
            return json.loads(r.text)
        else:
            return None

    def __getFollowCount(self,uk):
        toRequest = User.__request_url % (uk,1,0)
        r = requests.get(toRequest)
        if(r.status_code == 200):
            res = json.loads(r.text)
            return int(res['total_count'])
        else:
            return None

    def getCurrentPage(self):
        return self.__request_offset

    def __save(self,content):
        for item in content:
            item['uk'] = item['follow_uk']
            item['name'] = item['follow_uname']
            del item['follow_uname']
            del item['follow_uk']
            del item['follow_time']
            item['last_update'] = time.time()

            if self.__db.exist('user',{'uk':item['uk']}):
                continue
            else:
                self.__db.save(item)

    def spam(self,uk):
        count = self.__getFollowCount(uk)
        print count
        if count == None:
            return
        else:
            totalPage = count / User.__request_count + 1
            currentStart = 0
            for i in range(0,totalPage):
                content = self.__getJSONContent(uk,currentStart)
                self.__save(content['follow_list'])
                currentStart += self.__request_count

if __name__ == '__main__':
    log = Logger(u'用户信息获取:')
    user = User()
    log.info(user.spam(3458913532))
