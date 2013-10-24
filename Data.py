#-*-coding:utf-8-*-

from pymongo import MongoClient

class Data:

    def __init__(self,table):
        self.client = MongoClient()
        self.client = MongoClient('localhost',27017)
        self.db = self.client.baidu
        self.table = table

    def save(self,content):
        try:
            self.db[self.table].insert(content)
        except:
            print 'something error'

    def exist(self,table,query):
        if self.db[table].find_one(query):
            return True
        else:
            return False

if __name__ == '__main__':
    data = Data('Testing')
    data.save({"a":"c"})

