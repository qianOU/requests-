# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 22:15:24 2019

@author: HHj
"""
import requests
import re
from lxml import etree
class check_mark(object):
    
    def __init__(self,username,password,option,filename):
        self.username = username 
        self.password = password
        self.session = requests.Session()
        self.headers = {
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                 }
        self.option = option
        self.filename = filename
        
#模拟登陆的版块
    def login(self):
        #global c
        data ={
            "j_username": self.username,
            "j_password": self.password
              }
        
        
        str1='https://sso.shu.edu.cn/idp/profile/SAML2/POST/SSO'
        #访问百度搜索出来的上打教务管理系统的链接，因为发现点击这个链接有重定向的过程，需要捕获其中的隐藏的表单，
        w=self.session.get('https://oauth.shu.edu.cn/oauth/authorize?response_type=code&client_id=yRQLJfUsx326fSeKNUCtooKw&redirect_uri=http://cj.shu.edu.cn/passport/return&state=',allow_redirects = False)
        c=w.text
        data1={
                'SAMLRequest':'',
                 'RelayState':'',
               }   
        value = re.search(r'value=\"(.*?)\".*?value=\"(.*?)\"',w.text,re.S)
        data1['SAMLRequest'] = str(value.group(1))
        data1['RelayState'] = str(value.group(2))

        #得到隐藏的数据构造表单post方法进一步访问下一个重定向链接,里面有设置Cookie的成分
        response = self.session.post(str1,headers = self.headers,data=data1,allow_redirects=False,timeout=5)
        if response.status_code == 302:
            #cookies = requests.utils.dict_from_cookiejar(response.cookies)
            #print(response.url)
            跳转_url1 = response.headers['Location']
            #print('-'*40)
            #print('跳转_url1=',跳转_url1)
            #print('-'*30)


        #拿到Cookie以后，按照顺序访问下一个重定向链接，如果不访问则拿不到新的Cookie
        #此处不太懂为什么一定要访问下面这个网页
        response = self.session.get(跳转_url1,headers=self.headers,allow_redirects=False,timeout=5)
        跳转_url2 = response.headers['Location']
        #print('-'*40)
        #print('跳转_url2=',跳转_url2)
        #print('-'*30)
        
        
        #最后由上面步骤，已经拿齐了登陆页面所需要的所有Cookies,可以模拟提交用户名与密码了。
        response = self.session.post(跳转_url2,data=data,headers=self.headers,allow_redirects=False,timeout=5)
        #print(response.url)
        #if response.status_code == 302: 
            #print('='*35)
            #print(response.url)
            #print('='*35)
            #cookies = requests.utils.dict_from_cookiejar(response.cookies)
            #print(cookies)
            #print('='*35)
            
            
        #提交数据完成以后由有一系列Cookies的设定，都是通过不断的重定向来完成
        response = self.session.get('https://sso.shu.edu.cn/idp/profile/SAML2/POST/SSO',headers=self.headers,timeout=5)
        response.encoding = response.apparent_encoding
        c=response.text
        #此处也需要在重定向的链接中,取得隐藏的表单数据，只有拿到表单才能进一步发出正确的post请求
        text=re.search(r'name=\"RelayState\".*?=\"(.*?)\".*?name=\"SAMLResponse\".*?=\"(.*?)\"',c,re.S)
        str1 = text.group(1)
        str2 = text.group(2)
        data1={
                'RelayState':'',
                 'SAMLResponse':"",
              }
        data1['RelayState'] = str1.replace('&#x3a;',':').replace('&#x2f;','/').replace('&#x25;','%').replace('&#x3f;','?').replace('&#x3d;','=').replace('&amp;','&')
        data1['SAMLResponse'] = str2
      
        #由构造好的表达post请求下一个链接，下一个链接中会进一步设置Cookie信息
        response = self.session.post('http://oauth.shu.edu.cn/oauth/Shibboleth.sso/SAML2/POST',headers=self.headers,data = data1,allow_redirects=False,timeout=5)
        #print(response.cookies)
        #print('%'*40)
        
        #该链接中也会进一步设置Cookie信息
        response = self.session.get(data1['RelayState'],headers=self.headers,allow_redirects=False,timeout=5)
        #cookies=response.cookies
        url = response.headers['Location']
        #print(response.headers['Location'])
        #print('-'*50)
        
        #重定向到下个页面
        response = self.session.get(url,headers=self.headers,allow_redirects=False,timeout=5)
        #response = self.session.get('http://cj.shu.edu.cn/passport/return?code=807d3e023eb65306e25fb44b5ecb732d',headers=self.headers,allow_redirects=False)
        #cookies=response.cookies
        #response = requests.get('http://cj.shu.edu.cn/passport/return?code=807d3e023eb65306e25fb44b5ecb732d',headers=self.headers,allow_redirects=False,cookies=cookies)
        #print(response.cookies)
        
        #最终重定向到登陆成功的首页
        response = self.session.get(url,headers=self.headers,allow_redirects=True,timeout=5)
        #print(response.text)
        #res=self.session.get('http://cj.shu.edu.cn/Home/StudentIndex',headers=self.headers)
        #print(res.text)
        
        
        #进入首页，表明已经模拟登陆成功了，接下来就可以随心所欲了。。。。
        成绩查询_url = 'http://cj.shu.edu.cn/StudentPortal/CtrlScoreQuery'
        data = {
                'academicTermID': self.option
                }
        response=self.session.get(成绩查询_url,headers=self.headers,data = data,timeout=5)
        #print('+'*40)
        c=response.text
        return response.text


    #解析查询成绩的页面，并且写入文件之中
    def parse(self,sourse):
        with open(self.filename,'w',encoding='utf-8') as f:
            print('清空源数据！')
        text = etree.HTML(sourse)
        w={}
        w['person_info'] = text.xpath('//table/tr[1]/th//text()')
        w['person_info'] = [i.replace('\n','') for i in  w['person_info']]
        dict_1 = {"序号":'',"课程编号":"","课程名":"",
                          "学分":"","成绩":"","绩点":""}
        with open(self.filename,'a+',encoding='utf-8') as f:
            f.write(' '.join([i.replace('\xa0','').replace('\r','').replace('\n',' ') for i in w['person_info']]))
            f.write('\n')
        print(' '.join([i.replace('\xa0','').replace('\r','').replace('\n',' ') for i in w['person_info']]))
        for item in text.xpath('//table//tr[position()>2]')[:-1]:
            dict_1['序号'] = item.xpath('./td[1]/text()')[0]
            dict_1['课程编号'] = item.xpath('./td[2]/text()')[0]
            dict_1['课程名'] = item.xpath('./td[3]/text()')[0]
            dict_1['学分'] = item.xpath('./td[4]/text()')[0]
            dict_1['成绩'] = item.xpath('./td[5]/text()')[0]
            dict_1['绩点'] = item.xpath('./td[6]/text()')[0]
            print('序号:{0}  课程编号:{1}  课程名:{2}  学分:{3}  成绩:{4}  绩点:{5}'.format(
                    *list(dict_1.values())))
            print('-'*80)
            self.write(dict_1)
        print((' '.join([i.replace('\xa0','').replace('\r','').replace('\n',' ') for i in text.xpath('//table//tr[last()]/td//text()')])))
        with open(self.filename,'a+',encoding='utf-8') as f:
            f.write((' '.join([i.replace('\xa0','').replace('\r','').replace('\n',' ') for i in text.xpath('//table//tr[last()]/td//text()')])))
            f.write('\n')
        
    #将成绩写入文件中
    def write(self,dict_1):
        with open(self.filename,'a+',encoding='utf-8') as f:
            f.write('序号:{0}  课程编号:{1}  课程名:{2}  学分:{3}  成绩:{4}  绩点:{5}'.format(
                    *list(dict_1.values())))
            f.write('\n'+'-'*80+'\n')
            
#主函数如下：
def main():
    username,pwd =input('输入用户名,密码（以逗号分隔）=').split(',')
    option = input("""格式如下：年份+学期  学期=1：秋季学期   学期=2：冬季学期   学期=3：春季学期   学期=5：夏季学期\n例子：20182 表示 2018年冬季学期\n请输入查询的学期：""")
    #将文件保存到Score.txt中
    go = check_mark(username,pwd,option,'Score.txt')
    print('正在查询！请稍后...')
    text = go.login()
    if int(option[-1]) not in [1,2,3,5]:
        print('请输入正确的学期代号！！！')
    elif '本学期成绩未发布！' in text:
        print('查询本学期成绩中...')
    else:
         go.parse(text)
    
if __name__ == '__main__':
    main()
        
    
