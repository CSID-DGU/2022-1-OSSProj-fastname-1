#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup
import urllib.request
import ssl


# In[2]:


from dateutil.parser import parse
from urllib.request import urlopen
context=ssl._create_unverified_context()


# In[3]:


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


# In[4]:


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


# In[5]:


#링크 추출
link_bef=[]
for t in range(len(link_test)):
    link_address, title_name = link_test[t].split('">')
    link_ver1 = "https://www.dreamspon.com/" + link_address
    link_bef.append(link_ver1)


# In[6]:


# 행사 이름
titles_bef = []
for t in range(len(link_test)):
    link_address, title_name = link_test[t].split('">')
    titles_bef.append(title_name)


# In[7]:


# {"id":2,"first_name":"Brion","last_name":"Bonelle","email":"bbonelle1@mashable.com"}
dream_spon = []

for i in range(len(titles_bef)):
    li_tmp = {"title": titles_bef[i], "dday": dday_bef[i], "link": link_bef[i], "tag": tag[i]}
    dream_spon.append(li_tmp)


# In[8]:


dream = pd.DataFrame(dream_spon)
dream


# In[9]:


import json

with open('dream_spon.json', 'w', encoding="utf-8") as make_file: 
    json.dump(dream_spon, make_file, ensure_ascii = False, indent="\t")

