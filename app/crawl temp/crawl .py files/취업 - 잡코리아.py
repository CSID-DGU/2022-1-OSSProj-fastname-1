#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup
import re
import ssl


# In[2]:


from dateutil.parser import parse
from urllib.request import urlopen
context=ssl._create_unverified_context()


# In[3]:


links = []
titles = []
insts = []
end_list = []
base_url = 'http://www.jobkorea.co.kr'

# 페이지 개수 구해서 넘어가게
url= 'https://www.jobkorea.co.kr/starter/?chkSubmit=1&schCareer=&schLocal=&schPart=10016&schMajor=&schEduLevel=5&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt='
headers = {'User-Agent': 'Mozilla/5.0'} 
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
element_num = len(soup.select(' .tit > .link > span'))
cnt = int(soup.select(' #TabIngCount')[0].text.replace('(', '').replace(')', '').replace(',', ''))
if cnt % element_num == 0:
    page_num = cnt / element_num
else :
    page_num = int(cnt / element_num) + 1
    page_num = int(page_num)

for k in range(1,page_num+1):
    url= 'https://www.jobkorea.co.kr/starter/?chkSubmit=1&schCareer=&schLocal=&schPart=10016&schMajor=&schEduLevel=5&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=' + str(k) +'&schType=0&schGid=0&schOrderBy=0&schTxt='
    headers = {'User-Agent': 'Mozilla/5.0'} 
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
    length = len(soup.select(' div.tit > a '))
    for i in range(length):        
        titles.append(soup.select(' .tit > .link > span')[i].text)
        insts.append(soup.select(' .coTit > .coLink')[i].text)
        links.append(base_url + soup.select(' .tit > a')[i+1]['href'])
        end_list.append((soup.select(' .side > .day')[i].text).replace("~", ""))


# In[4]:


import json

job_korea = []

for i in range(len(titles)):
    li_tmp = {"title": titles[i], "d-day": end_list[i], "link": links[i], "기업": insts[i]}
    job_korea.append(li_tmp)

with open('job_korea.json', 'w', encoding="utf-8") as make_file: 
    json.dump(job_korea, make_file, ensure_ascii = False, indent="\t")

