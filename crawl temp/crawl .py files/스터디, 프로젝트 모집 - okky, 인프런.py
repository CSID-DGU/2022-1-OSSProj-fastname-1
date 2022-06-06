#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup
import re
import urllib.request

import datetime
from datetime import date, timedelta
from dateutil.parser import parse
from urllib.request import urlopen
import ssl


# In[17]:


context = ssl._create_unverified_context()
titles = []
dates = []
links = []
# li_tag = []
#main > section.community-body > div.community-body__content > div.question-list-container > ul > li:nth-child(20) > a
page_num = 1
# 24 48 72
for page_num in range(1, 3):
    url = 'https://www.inflearn.com/community/studies?page='+str(page_num)+'&status=unrecruited'
    req = urlopen(url, context=context)
    res = req.read()
    soup = BeautifulSoup(res,'html.parser')
    for i in range(0, 20):
        title = soup.select('.question__title > h3')[i].text.replace('\n', '').strip()
        dday = soup.select('.question__info-footer')[i].text.replace('\n', '')
        dday = dday.split('·', 1)[-1]
        dday = dday.lstrip().rstrip()
        if '시간' in dday or '분' in dday:
            dday = date.today()
        else:
            day_tmp = dday.split('일')[0]
            day_tmp = int(day_tmp)
            today = date.today()
            day_tmp = datetime.timedelta(days=day_tmp)
            dday = today - day_tmp
        dday = str(dday)
        year, month, day = dday.split('-')
        dday = year+'. '+month+'. '+day
        link = soup.select('.question-list-container > ul > li > a')[i]['href']
        titles.append(title)
        dates.append(dday)
        links.append('https://www.inflearn.com'+link)


# In[18]:


for i in titles:
    if i == '질문드립니다':
        num = titles.index(i)
        del titles[num]
        del links[num]
        del dates[num]


# In[19]:


context = ssl._create_unverified_context()
okky_titles = []
okky_dates = []
okky_links = []
# li_tag = []
not_good = ['종료', '완료', '마감']
page_num = 0
# 24 48 72
while(page_num<5):
    url = 'https://okky.kr/articles/gathering?offset='+str((page_num)*24)+'&max=24&sort=id&order=desc'
    req = urlopen(url, context=context)
    res = req.read()
    soup = BeautifulSoup(res,'html.parser')
    for i in range(4, 27):
        title = soup.select('.list-title-wrapper.clearfix > h5 > a')[i].text.replace('\n', '').lstrip().rstrip()
        dd = soup.select('div.date-created > span')[i].get_text()
        link = soup.select('.list-title-wrapper.clearfix > h5 > a')[i]['href']
        if (any(word in title for word in not_good) or len(title) < 3):
            continue
        else:
            okky_titles.append(title)
            okky_links.append('https://okky.kr'+link)
            dday = dd.split(" ")[0]
            year, month, day = dday.split('-')
            dday = year+'. '+month+'. '+day
            okky_dates.append(dday)

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


# In[20]:


for tmp in okky_links:
    url = tmp
    req = urlopen(url, context=context)
    res = req.read()
    soup = BeautifulSoup(res,'html.parser')
    bad = int(soup.select('.content-eval-count')[0].text)
    if bad < 0:
        num = okky_links.index(tmp)
        del okky_titles[num]
        del okky_links[num]
        del okky_dates[num]
    else: continue


# In[21]:


projects = []

titles = titles + okky_titles
dates = dates + okky_dates
links = links + okky_links

tags = []

for i in range(len(titles)):
    tag = []
    tmp = titles[i]
    if 'iOS' in tmp or '앱' in tmp or '게임' in tmp or '소프트웨어' in tmp or '응용' in tmp:        
        tag.append('응용')
    elif 'AI' in tmp or 'IoT' in tmp or '러닝' in tmp or '인공지능' in tmp:         
        tag.append('인공지능')
    elif '웹' in tmp or '엔드' in tmp or 'HTML' in tmp or 'web' in tmp:       
        tag.append('웹')
    elif '데이터' in tmp or 'DB' in tmp or 'Data' in tmp:      
        tag.append('데이터')
    elif '서버' in tmp or '블록체인' in tmp or '보안' in tmp:
        tag.append('서버')
    elif 'Unix' in tmp or 'Linux' in tmp or '임베디드' in tmp or '시스템' in tmp:
        tag.append('시스템')
    else:
        tag.append('기타')
          
    tags.append(tag)


# In[22]:


for i in range(len(okky_titles)):
    li_tmp = {"title": titles[i], "uploaded": dates[i], "link": links[i], "bigtag":tags[i]}
    projects.append(li_tmp)


# In[23]:


import json

with open('../json 결과/스터디.json', 'w', encoding="utf-8") as make_file: 
    json.dump(projects, make_file, ensure_ascii = False, indent="\t")

