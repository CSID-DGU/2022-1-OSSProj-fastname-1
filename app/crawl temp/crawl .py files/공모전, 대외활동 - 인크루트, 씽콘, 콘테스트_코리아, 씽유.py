#!/usr/bin/env python
# coding: utf-8

# In[7]:


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


# In[8]:


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
for i in range(1,13):
    try:
        inc_title.append(soup.select('#tbdyGmScrap > tr:nth-child('+str(i)+') > td.gmtitle > ul > a')[0].get_text())
        inc_host.append(soup.select('#tbdyGmScrap > tr:nth-child('+str(i)+') > td.company')[0].get_text().lstrip('\r\n\t\t\t\t\t\t\t').strip('\r\n\t\t\t\t\t\t\t'))
        inc_terms.append(soup.select('#tbdyGmScrap > tr:nth-child('+str(i)+') > td.due')[0].get_text())
        inc_links.append(soup.select('#tbdyGmScrap > tr:nth-child('+str(i)+') > td.gmtitle > ul > a')[0].get('href'))
    except:
        break


# In[9]:


inc_start_bef=[]
inc_end_bef=[]
for inc_term in inc_terms:
    inc_start_day,inc_end_day=inc_term.split("~")
    inc_start_bef.append('20'+inc_start_day.replace('.','. '))
    inc_end_bef.append('20'+inc_end_day.replace('.','. '))


# In[10]:


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


# In[11]:


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


# In[12]:


gongmo = []

for i in range(len(inc_title)):
    li_tmp = {"title": inc_title[i], "d-day": inc_end_bef[i], "link": inc_links[i], "tag": inc_host[i], "분류": "공모전"}
    gongmo.append(li_tmp)

for i in range(len(ck_title)):
    li_tmp = {"title": ck_title[i], "d-day": ck_date[i], "link": ck_link[i], "tag": ck_tag[i], "분류": "공모전"}
    gongmo.append(li_tmp)

for i in range(len(tc_links)):
    li_tmp = {"title": tc_titles[i], "d-day": end_date[i], "link": tc_links[i], "tag": participate[i], "분류": "공모전"}
    gongmo.append(li_tmp)


# In[13]:


d_title = []
title = []
d_link = []
link = []
d_date = []
date = []


# In[14]:


# 마감임박
for i in range (1, 3):
    cookies = {
        '_ga': 'GA1.3.435304916.1651484551',
        'ASPSESSIONIDSQDQCSCD': 'ADPANDLCOBGKHDGDNLALNONC',
        '_gid': 'GA1.3.1060530810.1652413738',
        '_gac_UA-163306206-1': '1.1652413738.Cj0KCQjw4PKTBhD8ARIsAHChzRJK1_Tf7OMLmorQhnztqqRBAgrge2dkQDsxtH0O7wbI3pKZgkkRg0QaAlDQEALw_wcB',
        'wcs_bt': 'fff9f7a878b278:1652413738',
    }

    headers = {
        'authority': 'thinkyou.co.kr',
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_ga=GA1.3.435304916.1651484551; ASPSESSIONIDSQDQCSCD=ADPANDLCOBGKHDGDNLALNONC; _gid=GA1.3.1060530810.1652413738; _gac_UA-163306206-1=1.1652413738.Cj0KCQjw4PKTBhD8ARIsAHChzRJK1_Tf7OMLmorQhnztqqRBAgrge2dkQDsxtH0O7wbI3pKZgkkRg0QaAlDQEALw_wcB; wcs_bt=fff9f7a878b278:1652413738',
        'origin': 'https://thinkyou.co.kr',
        'referer': 'https://thinkyou.co.kr/contest/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'pageSize': '35',
        'page': str(i),
        'serstatus': '0',
        'serfield': '5,6',
        'sertarget': '0',
        'serprizeMoney': '',
        'serdivision': '',
        'seritem': '',
        'searchstr': '',
    }
    response = requests.post('https://thinkyou.co.kr/contest/ajax_contestList.asp', cookies=cookies, headers=headers, data=data)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    length = soup.select('.title > a')
    for n in range(0, len(length)):
        name, host= soup.select('.title > a')[n].text.replace('\n', '').split('주최 :')
        start_date, end_date = soup.select('.etc')[2*n].text.split('~')
        links = length[n]['href']
        end_date = end_date.lstrip()
        d_date.append(end_date)
        d_title.append(name)
        d_link.append('https://thinkyou.co.kr/' + links)
    


# In[15]:


for i in range(len(d_title)):
    li_tmp = {"title": d_title[i], "d-day": d_date[i], "link": d_link[i], "분류": "대외활동"}
    gongmo.append(li_tmp)


# In[16]:


# 접수중
for i in range (1, 3):
    cookies = {
        '_ga': 'GA1.3.435304916.1651484551',
        'ASPSESSIONIDSQDQCSCD': 'ADPANDLCOBGKHDGDNLALNONC',
        '_gid': 'GA1.3.1060530810.1652413738',
        '_gac_UA-163306206-1': '1.1652413738.Cj0KCQjw4PKTBhD8ARIsAHChzRJK1_Tf7OMLmorQhnztqqRBAgrge2dkQDsxtH0O7wbI3pKZgkkRg0QaAlDQEALw_wcB',
        'wcs_bt': 'fff9f7a878b278:1652413738',
    }

    headers = {
        'authority': 'thinkyou.co.kr',
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_ga=GA1.3.435304916.1651484551; ASPSESSIONIDSQDQCSCD=ADPANDLCOBGKHDGDNLALNONC; _gid=GA1.3.1060530810.1652413738; _gac_UA-163306206-1=1.1652413738.Cj0KCQjw4PKTBhD8ARIsAHChzRJK1_Tf7OMLmorQhnztqqRBAgrge2dkQDsxtH0O7wbI3pKZgkkRg0QaAlDQEALw_wcB; wcs_bt=fff9f7a878b278:1652413738',
        'origin': 'https://thinkyou.co.kr',
        'referer': 'https://thinkyou.co.kr/contest/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'pageSize': '35',
        'page': str(i),
        'serstatus': '1',
        'serfield': '5,6',
        'sertarget': '0',
        'serprizeMoney': '',
        'serdivision': '',
        'seritem': '',
        'searchstr': '',
    }

    response = requests.post('https://thinkyou.co.kr/contest/ajax_contestList.asp', cookies=cookies, headers=headers, data=data)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    length = soup.select('.title > a')
    for n in range(0, len(length)):
        name, host= soup.select('.title > a')[n].text.replace('\n', '').split('주최 :')
        start_date, end_date = soup.select('.etc')[2*n].text.split('~')
        links = length[n]['href']
        end_date = end_date.lstrip()
        date.append(end_date)
        title.append(name)
        link.append('https://thinkyou.co.kr/' + links)

for i in range(len(title)):
    li_tmp = {"title": title[i], "d-day": date[i], "link": link[i], "분류": "대외활동"}
    gongmo.append(li_tmp)


# In[17]:


with open('공모전.json', 'w', encoding='UTF-8') as file:
     file.write(json.dumps(gongmo, ensure_ascii=False, indent="\t"))

