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

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import ssl

import time
from datetime import datetime


# In[2]:


import datetime
from dateutil.parser import parse
from urllib.request import urlopen
context=ssl._create_unverified_context()


# In[3]:


import datetime
import time


# In[10]:


"""
naming convention및 전처리 방법은  위 올콘과 동일함. 
"""

inc_title=[]
inc_host=[]
inc_terms=[]
inc_start_bef=[]
inc_end_bef=[]
inc_qualification=[]
inc_links=[]
inc_real_links=[]
base_url='https://gongmo.incruit.com/list/gongmolist.asp?ct=1&category=11'
webpage = urlopen(base_url,context=context)
soup = BeautifulSoup(webpage, 'html.parser')
for i in range(1,12):
    inc_title.append(soup.select('#tbdyGmScrap > tr:nth-child('+str(i)+') > td.gmtitle > ul > a')[0].get_text())
    inc_host.append(soup.select('#tbdyGmScrap > tr:nth-child('+str(i)+') > td.company')[0].get_text().lstrip('\r\n\t\t\t\t\t\t\t').strip('\r\n\t\t\t\t\t\t\t'))
    inc_terms.append(soup.select('#tbdyGmScrap > tr:nth-child('+str(i)+') > td.due')[0].get_text())
    inc_links.append(soup.select('#tbdyGmScrap > tr:nth-child('+str(i)+') > td.gmtitle > ul > a')[0].get('href'))
        


# In[ ]:


#tbdyGmScrap > tr:nth-child(1) > td.gmtitle
#tbdyGmScrap > tr:nth-child(11) > td.gmtitle


# In[11]:


inc_start_bef=[]
inc_end_bef=[]
for inc_term in inc_terms:
    inc_start_day,inc_end_day=inc_term.split("~")
    inc_start_bef.append('20'+inc_start_day.replace('.','. '))
    inc_end_bef.append('20'+inc_end_day.replace('.','. '))


# In[12]:


incuruit = []

for i in range(len(inc_title)):
    li_tmp = {"title": inc_title[i], "d-day": inc_end_bef[i], "link": inc_links[i], "tag": inc_host[i]}
    incuruit.append(li_tmp)


# In[14]:


import json

with open('incruit.json', 'w', encoding="utf-8") as make_file: 
    json.dump(incuruit, make_file, ensure_ascii = False, indent="\t")

