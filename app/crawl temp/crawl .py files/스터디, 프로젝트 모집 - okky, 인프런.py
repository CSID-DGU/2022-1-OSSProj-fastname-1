#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup
import re
import urllib.request

from dateutil.parser import parse
from urllib.request import urlopen
import ssl


# In[2]:


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
        date = soup.select('.question__info-footer')[i].text.replace('\n', '')
        uploader, date = date.split('·', 1)
        date = date.lstrip()
        link = soup.select('.question-list-container > ul > li > a')[i]['href']
        titles.append(title)
        dates.append(date)
        links.append('https://www.inflearn.com/'+link)


# In[3]:


for i in titles:
    if i == '질문드립니다':
        num = titles.index(i)
        del titles[num]
        del links[num]
        del dates[num]


# In[4]:


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
    for i in range(4, 28):
        title = soup.select('.list-title-wrapper.clearfix > h5 > a')[i].text.replace('\n', '').lstrip().rstrip()
        dd = soup.select('div.date-created > span')[i].get_text()
        link = soup.select('.list-title-wrapper.clearfix > h5 > a')[i]['href']
        if (any(word in title for word in not_good) or len(title) < 3):
            continue
        else:
            okky_titles.append(title)
            okky_links.append('https://okky.kr'+link)
            day, write_time = dd.split(" ")
            okky_dates.append(day)

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


# In[5]:


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


# In[6]:


projects = []

for i in range(len(titles)):
    li_tmp = {"title": titles[i], "dday": dates[i], "link": links[i]}
    projects.append(li_tmp)


# In[7]:


for i in range(len(okky_titles)):
    li_tmp = {"title": okky_titles[i], "uploaded": okky_dates[i], "link": okky_links[i]}
    projects.append(li_tmp)


# In[8]:


import json

with open('projects.json', 'w', encoding="utf-8") as make_file: 
    json.dump(projects, make_file, ensure_ascii = False, indent="\t")

