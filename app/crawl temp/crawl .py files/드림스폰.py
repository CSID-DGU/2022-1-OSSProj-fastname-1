#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import csv

import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import time
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import ssl
import time
from datetime import datetime


# In[3]:


import datetime
from dateutil.parser import parse
from urllib.request import urlopen
context=ssl._create_unverified_context()


# In[4]:


import datetime
import time


# In[31]:


#드림스폰 일반 공모전 D-DAY 크롤링

dday_bef = []
tag = []
page_num = 1
while(page_num <=5):        
    url = 'https://www.dreamspon.com/scholarship/list.html?page='+str(page_num)+'&ordby=1'
    req = urllib.request.urlopen(url)
    res = req.read()
    soup = BeautifulSoup(res,'html.parser')
    days = soup.select(" .td_day > .count")
    target = soup.select(".hashtag")
    for i in range(len(days)):
        dday_bef.append((days[i].text))
        tag_tmp = ((target[i].get_text()).replace("#", "").replace("\n", " "))
        tag_tmp = tag_tmp.strip()
        tag_tmp = tag_tmp.split(" ")
        tag.append(tag_tmp)
    page_num += 1  


# In[32]:


link_test = []
page_num = 1
while(page_num <=5):        
    url = 'https://www.dreamspon.com/scholarship/list.html?page='+str(page_num)+'&ordby=1'
    req = urllib.request.urlopen(url)
    res = req.read()
    soup = BeautifulSoup(res,'html.parser')
    contests = soup.find_all("p",class_="title")
    days = soup.select(" .td_day > .count")        
    for i in range(len(days)):
        link_test.append(str(contests[i]).strip('[<p class="title"><a href="').strip('</a>'))
    page_num += 1    


# In[33]:


#링크 추출
link_bef=[]
for t in range(len(link_test)):
    link_address, title_name = link_test[t].split('">')
    link_ver1 = "https://www.dreamspon.com/" + link_address
    link_bef.append(link_ver1)


# In[34]:


# 행사 이름
titles_bef = []
for t in range(len(link_test)):
    link_address, title_name = link_test[t].split('">')
    titles_bef.append(title_name)


# In[35]:


# {"id":2,"first_name":"Brion","last_name":"Bonelle","email":"bbonelle1@mashable.com"}
dream_spon = []

for i in range(len(titles_bef)):
    li_tmp = {"title": titles_bef[i], "d-day": dday_bef[i], "link": link_bef[i], "tag": tag[i]}
    dream_spon.append(li_tmp)


# In[36]:


dream = pd.DataFrame(dream_spon)
dream


# In[39]:


import json

with open('dream_spon', 'w', encoding="utf-8") as make_file: 
    json.dump(dream_spon, make_file, ensure_ascii = False, indent="\t")

