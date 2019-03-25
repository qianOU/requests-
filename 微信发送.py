# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:10:25 2019

@author: Administrator
"""
import itchat
from 成绩查询 import check_mark
import time


class Send(object):
    def __init__(self,name,filename):
        self.user = name
        self.filename = filename
        
    def send_info(self):
        itchat.auto_login(hotReload = True)
        user = itchat.search_friends(name = self.user)[0]
        itchat.send('成绩发布啦！,请查看下面的文件：',toUserName = user['UserName'])
        itchat.send_file(fileDir = self.filename,toUserName = user['UserName'])
        
def main(name,filename):
    #选择微信用户
    with open(filename,encoding ='utf-8') as f:
        f.close()
    target = Send(name,filename)
    print(target)
    username,pwd =input('输入用户名,密码（以逗号分隔）=').split(',')
    option = input("""格式如下：年份+学期  学期=1：秋季学期   学期=2：冬季学期   学期=3：春季学期   学期=5：夏季学期\n例子：20182 表示 2018年冬季学期\n请输入查询的学期：""")
    go = check_mark(username,pwd,option,filename)
    print('正在查询！请稍后...')
    while True:
        try:
             text = go.login()
             if int(option[-1]) not in [1,2,3,5]:
                 print('请输入正确的学期代号！！！')
             elif '本学期成绩未发布！' in text:
                 print('成绩未发布！持续更新中...')
                 time.sleep(8)
                 continue
#                 print('查询本学期成绩中...')
#                 time.sleep(1)
             else:
                 go.parse(text)
                 break
        except Exception:
            print('成绩未发布！持续更新中...')
            time.sleep(8)
            continue
            
    target.send_info()
    return 1

def Main(name):
    while True:
         if main(name,'Score.txt'):
             print('successful!')
             break
         
if __name__ == '__main__':
    #昵称不是备注，也不是微信号哦
     Main('微信中的目标接受人的昵称')
     
     

    
         
