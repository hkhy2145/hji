import urllib.request
import re
import os
import re
import subprocess
import time
import sys
import random
import requests
from subprocess import Popen , PIPE
import threading
from fake_useragent import UserAgent
ua=UserAgent()
def chesk(url):
    block_url=["google.com","bing.com","microsoft.com","amazon","youtube","facebook","ask.com"]
    for i in block_url:
        #print(i)
        if i in url :
            #print("e")
            return False
        
    #print("t")
    return True
def sqli_targ(url):
    try:
        k=re.findall("(/.*?=)",url)
        return len(k)>=1
    except:
        return False
def scrap_url(se,resp_data):
    if se=="google":#<<scrap url from google resultin and save url>>
        u=re.findall(r"<a(.*?)</a>", resp_data)
        for i in u:
            urls = re.findall(r"(http.*?)&", i)#re.findall(r"&url=(http?.*?)&", resp_data)#re.findall(r"q=(https:?//.*?)&sa", resp_data)#re.findall(r'<a href="(https?://.*?)"', resp_data)
            if len(urls)>=1 and chesk(str(urllib.parse.unquote(urls[0]))) and sqli_targ(str(urllib.parse.unquote(urls[0]))):
                open('reusltn\\google_res.txt', '+a', encoding='utf-8').write(str(urllib.parse.unquote(urls[0]))+'\n')            
    if se=="bing":#<<scrap url from bing resultin and save url>>
        u=re.findall(r"<a(.*?)</a>", resp_data)
        for i in u:
            ###print("------------------")
            urls = re.findall(r'href="(http.*?)" h=', i)            
            if len(urls)>=1 and chesk(str(urllib.parse.unquote(urls[0]))) and sqli_targ(str(urllib.parse.unquote(urls[0]))):
                #print(urls)
                open('reusltn\\bing_res.txt', '+a', encoding='utf-8').write(str(urllib.parse.unquote(urls[0]))+'\n')
    if se=="ask":#<<scrap url from bing resultin and save url>>
        u=re.findall(r'target="_blank"(.*?)-unified', resp_data)
        for i in u:
            urls = re.findall(r"href='(http.*?)' data", i)
            if len(urls)>=1 and chesk(str(urllib.parse.unquote(urls[0]))) and sqli_targ(str(urllib.parse.unquote(urls[0]))):
                open('reusltn\\ask_res.txt', '+a', encoding='utf-8').write(str(urllib.parse.unquote(urls[0]))+'\n')
def next_page(resp_data,se):
    if se=="bing":
        np=next_page_list=re.findall(r"first=(.*?)&", resp_data)#first=51&
        np=list(set(np))
        try:
            np.remove('0')
        except:
            pass
        return np
def get_respons(url):#<<get resultin from url>>
    print(url)
    #print(url)
    try:
        headers = {'User-Agent': ua.chrome}
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        resp_data = resp.read().decode('utf-8')
        return resp_data
    except:
        resp_data=''
        return resp_data
def search_google(query):#<<making google url and scrap data>>
    query = query.replace(' ', '+')
    url = "https://www.google.com/search?q=%s&num=200&hl=en&complete=0&safe=off&filter=0&btnG=Search&start=0"%query
    resp_data=get_respons(url)
    #open(f'google_search_results.html', 'w', encoding='utf-8').write(resp_data)
    scrap_url("google",resp_data)
def search_bing(query):#<<making bing url and scrap data>>
    query = query.replace(' ', '+')
    url='https://www.bing.com/search?q=%s&count=200&first=0'%query
    ##print(url)
    resp_data=get_respons(url)
    #open('bing_search_results.html', 'w', encoding='utf-8').write(resp_data)
    if len(resp_data)==154660:
        scrap_url("bing",resp_data)
        np=next_page(resp_data,"bing")
        for i in np:
            url=f'https://www.bing.com/search?q=%s&rdr=1&count=200&first={i}'%query
            resp_data=get_respons(url)
            ##print(len(resp_data))
            if len(resp_data)==154660:
                scrap_url("bing",resp_data)
        #open('reusltn\\bing_search_results2.html', 'w', encoding='utf-8').write(resp_data)
def search_ask(query):#<<making ask url and scrap data>>
    query = query.replace(' ', '+')
    for i in range(1,5):
        url=f'https://www.ask.com/web?q=%s&page={i}'%query
        resp_data=get_respons(url)
        if len(resp_data)>80000:
            ##print(len(resp_data))
            scrap_url("ask",resp_data)
            #open(f'ask_search_results{i}.html', 'w', encoding='utf-8').write(resp_data)
dork=open("dork.txt","+r",encoding="utf-8").readlines()
#dork=["site:*.edu inurl:?ITEM_ID="]
co=["edu.in","edu.pl","edu.br","edu","gov","edu.au","edu.hk","edu.eg","edu.vn","edu.sa","edu.om","edu.jo","edu.au","edu.my","edu.sg","ac.th"]

for query in dork:
    for i in co:
        query1=query
        query1=f"site:*.{i} inurl:"+query[:-1]
#         #print(query1)
#         #print("---")
        requests.get("http://127.0.0.1:8080/api/message?key=secret_key&msg=s")
        search_google(query1)
        search_ask(query1)
        query2='inurl:"'+query[:-1]+f'" site:.{i}'
#         print(query2)
#         #print("---")
        search_bing(query2)
        
    


# save the response
# with open('google_search_results.html', 'w', encoding='utf-8') as f:
#     f.write(resp_data)

# save the list of URLs
# with open('google_search_urls.txt', 'w', encoding='utf-8') as f:
#     for url in urls:
#         url=urllib.parse.unquote(url)
#         f.write(url + '\n')


