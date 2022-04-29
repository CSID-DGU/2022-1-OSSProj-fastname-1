#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import json
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver

url = 'https://www.contestkorea.com/sub/list.php?int_gbn=1&Txt_bcode=030210001'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    list_crawl = soup.select('#frm > div > div.list_style_2 > ul')
    print(list_crawl)

else : 
    print(response.status_code)


# In[4]:


result = {
    "title": [],
    "date" : [],
    "category": []
}

for li in list_crawl:
    for num in range(0, 11):
        try:
            li_title = li.select('li > div.title > a > span.txt')[num].get_text()
            li_date_tmp = li.select('li > div.date > div > span.step-1')[num].text
            li_date = li_date_tmp.replace("\n", "").replace("\t", "")
                    
            result["title"].append(li_title)
            result["date"].append(li_date)
            
        except IndexError:
            continue
            
    for no in range(0, 11):
        li_tmp = li.select('li')[3*no]
        tmp = []
        for i in range(0, 5):
            try:
                cat = li_tmp.select('div.title > a > span.category')[i].get_text()
                tmp.append(cat)
            except IndexError:
                continue
        result["category"].append(tmp)


# In[5]:


for key, value in result.items():
    print(key, value)


# In[7]:


import json

print(json.dumps(result, ensure_ascii=False, indent="\t"))
# JSON 생성 시 형태 확인


# In[9]:


with open('result.json', 'w', encoding="utf-8") as make_file: 
    json.dump(result, make_file, ensure_ascii = False, indent="\t")

