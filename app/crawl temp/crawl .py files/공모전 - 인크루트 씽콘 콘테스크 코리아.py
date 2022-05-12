#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import urllib.request
import ssl
from dateutil.parser import parse
from urllib.request import urlopen
import json
import requests
context=ssl._create_unverified_context()


# In[4]:


# 공모전 인크루트
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


# In[5]:


inc_start_bef=[]
inc_end_bef=[]
for inc_term in inc_terms:
    inc_start_day,inc_end_day=inc_term.split("~")
    inc_start_bef.append('20'+inc_start_day.replace('.','. '))
    inc_end_bef.append('20'+inc_end_day.replace('.','. '))


# In[ ]:


# 공모전 콘테스트 코리아
ck_title = []
ck_date = []
ck_link = []
ck_tag = []
ck_target = ['대학생', '일반인', '누구나']

for n in range(1, 6):
    url = ('https://www.contestkorea.com/sub/list.php?displayrow=12&int_gbn=1&Txt_sGn=1&Txt_key=all&Txt_word=&Txt_bcode=030210001&Txt_code1=&Txt_aarea=&Txt_area=&Txt_sortkey=a.int_sort&Txt_sortword=desc&Txt_host=&Txt_tipyn=&Txt_actcode=&page='+str(n))
    headers = {'User-Agent': 'Mozilla/5.0'} 
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')

   
    list_crawl = soup.select('#frm > div > div.list_style_2 > ul')

    for li in list_crawl:        
        for num in range(0, 12):
            tmp = []
            try:
                li_target = li.select('li > ul > li.icon_2')[num].get_text().replace('\t', '').replace('\n', '')
                if any(word in li_target for word in ck_target):
                    li_title = li.select('li > div.title > a > span.txt')[num].get_text()
                    li_date_tmp = li.select('li > div.date > div > span.step-1')[num].text
                    li_date = li_date_tmp.replace("\n", "").replace("\t", "")
                    link_tmp = li.select('li > div.title > a')[num]
                    link_tmp = link_tmp['href']               
                    ck_title.append(li_title)
                    ck_date.append(li_date)
                    ck_link.append("https://www.contestkorea.com/sub/" + link_tmp)
                else:            
                    continue         
            except IndexError:
                break
            
            try:
                li_tmp = li.select('li')[3*num]
            except IndexError:
                break          
            for i in range(0, 5):
                try:
                    cat = li_tmp.select('div.title > a > span.category')[i].get_text()
                    tmp.append(cat)
                except IndexError:
                    break    
            ck_tag.append(tmp)


# In[ ]:


# 공모전 씽콘
url_base = 'https://www.thinkcontest.com/Contest/CateField.html?page=1&c=11'
headers = {'User-Agent': 'Mozilla/5.0'}
res = requests.get(url_base, headers=headers)
soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
key = ['과학/공학', '게임/소프트웨어']
tc_links = []
tc_titles = []
tc_dday = []
tc_inst = []
tc_dates = []
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
            tc_titles.append(soup.select(' .txt-left > .contest-title > a')[i].text)
            tc_links.append(base_url + soup.select('.txt-left > .contest-title > a ')[i]['href'])
            tc_dday.append(soup.select(' td > p ')[i].text.split('-')[1])
    k=k+1
                            
str_date = []
end_date = []
participate = []
for i in range(len(tc_links)):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(tc_links[i], headers=headers)
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
    tc_inst.append(soup.select(' tbody > tr > td ')[0].text)


# In[6]:


incuruit = []
for i in range(len(inc_title)):
    li_tmp = {"title": inc_title[i], "d-day": inc_end_bef[i], "link": inc_links[i], "tag": inc_host[i]}
    incuruit.append(li_tmp)

Contest_korea = []
for i in range(len(ck_title)):
    li_tmp = {"title": ck_title[i], "d-day": ck_date[i], "link": ck_link[i], "tag": ck_tag[i]}
    Contest_korea.append(li_tmp)

think_con = []

for i in range(len(tc_links)):
    li_tmp = {"title": tc_titles[i], "d-day": end_date[i], "link": tc_links[i], "tag": participate[i]}
    think_con.append(li_tmp)


# In[7]:


with open('incruit.json', 'w', encoding="utf-8") as make_file: 
    json.dump(incuruit, make_file, ensure_ascii = False, indent="\t")

with open('think_con.json', 'w', encoding="utf-8") as make_file: 
    json.dump(think_con, make_file, ensure_ascii = False, indent="\t")

with open('Contest_korea.json', 'w', encoding="utf-8") as make_file: 
    json.dump(Contest_korea, make_file, ensure_ascii = False, indent="\t")

