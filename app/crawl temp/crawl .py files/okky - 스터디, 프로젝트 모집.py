#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup
import re
import urllib.request

from dateutil.parser import parse
from urllib.request import urlopen


# In[7]:


import ssl

context = ssl._create_unverified_context()
titles = []
date = []
links = []
# li_tag = []
not_good = ['종료', '완료', '마감']

page_num = 0
# 24 48 72
while(page_num<5):
    url = 'https://okky.kr/articles/gathering?offset='+str((page_num)*24)+'&max=24&sort=id&order=desc'
    req = urlopen(url, context=context)
    res = req.read()
    soup = BeautifulSoup(res,'html.parser')
    for i in range(4, 28):
        title = soup.select('.list-title-wrapper.clearfix > h5 > a')[i].text.replace('\n', '').lstrip().rstrip()
        dd = soup.select('div.date-created > span')[i].get_text()
        link = soup.select('.list-title-wrapper.clearfix > h5 > a')[i]['href']
        if (any(word in title for word in not_good) or len(title) < 3):
            continue
        else:
            titles.append(title)
            links.append('https://okky.kr'+link)
            day, write_time = dd.split(" ")
            date.append(day)

            # 태그를 추출해 추가하기에는 페이지에서 보여지는 태그가 애매하다.
            # 따로 키워드를 선정하거나 할 필요가 있어보임
            '''
            for j in range(1, 8):
                tmp = []
                try:
                    tag = soup.select('#list-article > div.panel.panel-default.gathering-panel > ul > li:nth-child('+str(i-3)+') > div.list-title-wrapper.clearfix > div > a')[j].get_text()
                    tmp.append(tag)
                except:
                    continue
                li_tag.append(tmp)
            '''
       
           
    page_num+=1


# In[8]:


# 반응이 나쁜 게시물 제거
for tmp in links:
    url = tmp
    req = urlopen(url, context=context)
    res = req.read()
    soup = BeautifulSoup(res,'html.parser')
    bad = int(soup.select('.content-eval-count')[0].text)
    if bad < 0:
        num = links.index(tmp)
        del titles[num]
        del links[num]
        del date[num]
    else: continue


# In[9]:


okky = []

for i in range(len(titles)):
    li_tmp = {"title": titles[i], "d-day": date[i], "link": links[i]}
    okky.append(li_tmp)

df = pd.DataFrame(okky)
df


# In[10]:


import json

with open('okky.json', 'w', encoding="utf-8") as make_file: 
    json.dump(okky, make_file, ensure_ascii = False, indent="\t")

