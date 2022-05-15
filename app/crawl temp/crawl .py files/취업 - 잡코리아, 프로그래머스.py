#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pandas import json_normalize
import numpy as np

import requests
from bs4 import BeautifulSoup
import re
import ssl
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

job = []

for i in range(len(titles)):
    li_tmp = {"title": titles[i], "d-day": end_list[i], "link": links[i], "기업": insts[i]}
    job.append(li_tmp)


# In[5]:


# 취업 프로그래머스
pr_titles = []
pr_company = []
pr_links = []
pr_address = []

for i in range(1, 27):

    cookies = {
        '_programmers_session_production': '8afb764fc54ea3576ad07db48d3c723c',
        '_gcl_au': '1.1.1544457234.1651487879',
        '_ga': 'GA1.3.2065482246.1651487879',
        '_fbp': 'fb.2.1651487879006.854201146',
        '__gads': 'ID=293401b0ae4479e9-2250976589d20099:T=1651487879:RT=1651487879:S=ALNI_MZ_oVdweVxKkRrx9a57H3W4jvqWYg',
        '_gcl_aw': 'GCL.1652522688.Cj0KCQjwpv2TBhDoARIsALBnVnn-ySzmgtkyQtwrJCDvQjJ1XGSP5L7VBwRXHGKO0_kgNhlYdQEK21oaApg7EALw_wcB',
        '_gid': 'GA1.3.50921043.1652522688',
        '_gac_UA-72680702-5': '1.1652522688.Cj0KCQjwpv2TBhDoARIsALBnVnn-ySzmgtkyQtwrJCDvQjJ1XGSP5L7VBwRXHGKO0_kgNhlYdQEK21oaApg7EALw_wcB',
        '_clck': 'd6s3xo|1|f1g|0',
        'locale': 'ko',
        '_gat_UA-72680702-5': '1',
        '_clsk': '1uba3yj|1652542257360|7|1|h.clarity.ms/collect',
    }

    headers = {
        'authority': 'programmers.co.kr',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_programmers_session_production=8afb764fc54ea3576ad07db48d3c723c; _gcl_au=1.1.1544457234.1651487879; _ga=GA1.3.2065482246.1651487879; _fbp=fb.2.1651487879006.854201146; __gads=ID=293401b0ae4479e9-2250976589d20099:T=1651487879:RT=1651487879:S=ALNI_MZ_oVdweVxKkRrx9a57H3W4jvqWYg; _gcl_aw=GCL.1652522688.Cj0KCQjwpv2TBhDoARIsALBnVnn-ySzmgtkyQtwrJCDvQjJ1XGSP5L7VBwRXHGKO0_kgNhlYdQEK21oaApg7EALw_wcB; _gid=GA1.3.50921043.1652522688; _gac_UA-72680702-5=1.1652522688.Cj0KCQjwpv2TBhDoARIsALBnVnn-ySzmgtkyQtwrJCDvQjJ1XGSP5L7VBwRXHGKO0_kgNhlYdQEK21oaApg7EALw_wcB; _clck=d6s3xo|1|f1g|0; locale=ko; _clsk=1uba3yj|1652542257360|7|1|h.clarity.ms/collect; _gat_UA-72680702-5=1',
        'referer': 'https://programmers.co.kr/job?page=3&min_career=0&order=recent',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': 'bf5ca34edda74dbd9e694288d7f28313-9877ff800e5309db-0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
    }

    response = requests.get('https://programmers.co.kr/api/job_positions?min_career=0&order\\[\\]=recent&page='+str(i), cookies=cookies, headers=headers)

    html = response.text
    dict = json.loads(html)
    df = json_normalize(dict['jobPositions'])
    df = df.drop(['careerRange', 'companyId', 'jobType', 'maxSalary', 'minSalary', 'personalized', 'signingBonus', 'company.revenue', 'company.hideRevenue', 'company.blog', 'company.funding', 'company.hideFunding', 'company.countryCode', 'careerOption', 'jobCategoryIds', 'createdAt',
    'career', 'startAt', 'updatedAt', 'company.serviceUrl' ,'company.logoUrl' ,'company.employees', 'company.developers', 'company.employeesCount', 'company.averageResponseTime', 'company.id', 'status', 'company.serviceName', 'company.homeUrl', 'company.address', 'id', 'period', 'technicalTags',
    'company.benefitTags', 'teamTechnicalTags'], axis=1)
    df = df[['title', 'company.name', 'url', 'address']]

    for i in range(len(df)):
        title = df.iloc[i][0]
        name = df.iloc[i][1]
        link = df.iloc[i][2]
        link = 'https://programmers.co.kr'+str(link)
        pr_titles.append(title)
        pr_company.append(name)
        pr_links.append(link)


# In[ ]:


for i in range(len(pr_titles)):
    li_tmp = {"title": pr_titles[i], "d-day": '해당없음', "link": pr_links[i], "기업": pr_company[i]}
    job.append(li_tmp)

with open('취업.json', 'w', encoding="utf-8") as make_file: 
    json.dump(job, make_file, ensure_ascii = False, indent="\t")

