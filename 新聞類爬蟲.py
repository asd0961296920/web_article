import requests
from bs4 import BeautifulSoup
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
import pandas as pd
import numpy as np
import json
from fake_useragent import UserAgent
from pygtrans import Translate
import os
client = Translate()


ua = UserAgent()


def wordpress(tabb,pot):
        #網站登入資訊
    id="asd0961296920"
    password="xz25285132"
    
    #網站網址，請把example.com替換成你的網址，並且先試著連上該網址，應該會出現「XML-RPC server accepts POST requests only.」才對。
    url="https://mak.nde.tw/xmlrpc.php"
    
    #新文章要直接發布的話，就不用改，如果要變成草稿，就改成"draft"
    which="publish"
    #which="draft"


           #建立客戶端
    print('開始上傳')
    try:
        wp = Client(url, id,password)
                
            #建立新文章
        post = WordPressPost()
        post.post_status = which
        post.title = tabb
        post.content = pot
        post.terms_names = {
        "category": ["current-news"]
        }
                
                #如果這一篇是過去的文章，可以透過這個方式指定該文章發表的日期。
                #post.date=datetime.strptime("2018/1/01 10:05:10","%Y/%m/%d %H:%M:%S")
                #發出去!
        wp.call(NewPost(post))
        print('上傳完畢')

    except:
        fr = input('錯誤 無法上傳請更換代理:')
        if(fr == 'd'):
            print('程式停止')
            os._exit()
            
            
        #wordpress(tabb,pot)
        
    
    
    
    
    
        



def translate(word):
    # 有道词典 api
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        return response.text
    else:
        print("有道词典调用失败")
        # 相应失败就返回空
        return None
 
 
def get_main(word):
    list_trans = translate(word)
    result = json.loads(list_trans)
    result = result['translateResult'][0][0]['tgt']
    return result

#调用































d = 8
while d<16 :

    sz = 1

    #標題連接部分
    ua = UserAgent()
    ttr=True
    while(ttr):
        

         try:
            print('第'+str(d)+'頁開始搜尋')
            r = requests.get('https://www.sinovision.net/home/space/uid/3453/do/blog/view/me/from/space/page/'+str(d)+'.html', headers={
        "User-Agent": ua.random
    })
            ttr= False
         except:
            
            input("標題代理ip失效請更換代理:")
            
        
        
    r.encoding = 'utf-8'
    soups = BeautifulSoup(r.text, "html.parser")
    cc1 = soups.find_all("dt", class_="xs2")

#標題處理部分

    for ccs in cc1:
        xz = ccs.find("a",target="_blank").get("href")
        xz2 = ccs.find("a",target="_blank").getText()
        rrs = get_main(xz2)
        print('標題搜尋完成')
        ua = UserAgent()  
        
    #內容網路連接
        ttr = True
        while(ttr):
            
            try:
                print('內容開始搜尋')
                tt2 = []
                tt = ''
                r = requests.get(xz, headers={
                        "User-Agent": ua.random
                    })
                ttr = False
            except:
                ipcon = input("內容代理ip失效請更換代理:")
                

        r.encoding = 'utf-8'
        soups = BeautifulSoup(r.text, "html.parser")
        cc = soups.find_all("div", class_="d cl")
        v= 0
    
    #內容處理部分
        
        for ccse in cc:
            xzz = ccse.find_all("font")
            
            
            for xzs in xzz:
                
                
                
                
                if(xzs.select_one("img") != None  ):
                    
        
                    tt2.append(xzs.select_one("img").get("src"))
                    tt +='@'+str(v)
                    v = v+1
                    
                    
                tt += xzs.getText()
        
                
        tt = client.translate(tt, target='en')
        tte = tt.translatedText
        tte = tte.replace('.', '.\n\n')
        for i in range(v):
            tte = tte.replace('@'+str(i), '<figure class=\"wp-block-image size-large\"><img src=\"'+tt2[i]+'\" width=\"500\" height=\"500\"></figure>')

        wordpress(rrs,tte)
        time.sleep(20)
        print('第'+str(sz)+'篇文章上傳完成')
        sz = sz+1                



            
            
            
            

    print('第'+str(d)+'頁搜尋完成')
            
            
    time.sleep(1)
    d=d+1
print('搜尋結束')

