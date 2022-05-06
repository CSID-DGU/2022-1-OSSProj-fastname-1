#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import csv

import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import time
from time import sleep
from urllib.request import urlopen

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import ssl
context=ssl._create_unverified_context()

import time
from datetime import datetime


# In[2]:


import datetime
from dateutil.parser import parse


# In[5]:



url_base = 'https://www.thinkcontest.com/Contest/CateField.html?page=1&c=11'
headers = {'User-Agent': 'Mozilla/5.0'}
res = requests.get(url_base, headers=headers)
soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
key = ['과학/공학', '게임/소프트웨어']
links = []
titles = []
dday = []
inst = []
dates = []
k = 1
    
while k <= 10:
    url = 'https://www.thinkcontest.com/Contest/CateField.html?page=' + str(k) + '&c=11'
    base_url = 'https://www.thinkcontest.com/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
    len_link = len(soup.select(' .txt-left > .contest-title > a'))
    for i in range(len_link):
        if soup.select(' td > span ')[i].text.replace('\n', '') == '마감':
            break
        else:
            titles.append(soup.select(' .txt-left > .contest-title > a')[i].text)
            links.append(base_url + soup.select('.txt-left > .contest-title > a ')[i]['href'])
            dday.append(soup.select(' td > p ')[i].text.split('-')[1])
    k=k+1
                            
str_date = []
end_date = []
participate = []
for i in range(len(links)):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(links[i], headers=headers)
    soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
    html = soup.select(' tr')
    text = str(html).replace('\n', '')
    certi = re.compile('참가자격' + '.{200}')
    test = certi.findall(text)[0]
    partis = []
    if '제한없음' in test:
        partis.append('대학(원)생')
        pass
    elif '일반인' in test:
        partis.append('대학(원)생')
        pass
    elif '국내외 석학과 연구진' in test:
        partis.append('대학원생')
        pass
    elif '대학생' in test:
        if '대학원생' in test:
            partis.append('대학(원)생')
            pass
        else :
            partis.append('대학생')
            pass
    elif '대학원생' in test:
        partis.append('대학원생')
    else : 
        pass
            

    participant = str(partis).replace('[', '').replace(']', '').replace("'", "")
    start = re.compile('접수기간' + '.{19}')
    strdate = start.findall(text)[0].split('<td>')[1]
    end = re.compile('접수기간' + '.{32}')
    enddate = end.findall(text)[0].split('~')[1].replace(' ', '')
    participate.append(participant)
    str_date.append(strdate)
    end_date.append(enddate)
    inst.append(soup.select(' tbody > tr > td ')[0].text)
        
        
think_con = []

for i in range(len(links)):
    li_tmp = {"title": titles[i], "d-day": end_date[i], "link": links[i], "tag": participate[i]}
    think_con.append(li_tmp)


# In[ ]:


#titles 제목
#end_date 마감일
#participate 참가자격
#links 링크


# In[7]:


import json

with open('think_con.json', 'w', encoding="utf-8") as make_file: 
    json.dump(think_con, make_file, ensure_ascii = False, indent="\t")

