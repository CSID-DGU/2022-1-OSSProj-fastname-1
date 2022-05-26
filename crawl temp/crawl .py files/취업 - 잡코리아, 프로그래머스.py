#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
from pandas import json_normalize
import numpy as np

import requests
from bs4 import BeautifulSoup
import re
import ssl
import datetime
from datetime import date, timedelta
from dateutil.parser import parse
from urllib.request import urlopen
context=ssl._create_unverified_context()


# In[29]:


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
        dday = (soup.select(' .side > .day')[i].text).replace("~", "")
        dday = dday.split('(')[0]
        try:
            year, month, day = dday.split('.')
            dday = year+'. '+month+'. '+day
        except:
            end_list.append(dday)
        end_list.append(dday)


# In[30]:


import json

job = []

for i in range(len(titles)):
    li_tmp = {"title": titles[i], "dday": end_list[i], "link": links[i], "기업": insts[i]}
    job.append(li_tmp)


# In[31]:


# 취업 프로그래머스
pr_titles = []
pr_company = []
pr_links = []
pr_address = []
pr_dday = []

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


# In[32]:


for i in pr_links:
    id = i.split('/')[-1]
    cookies = {
        '_programmers_session_production': '8afb764fc54ea3576ad07db48d3c723c',
        '_gcl_au': '1.1.1544457234.1651487879',
        '_ga': 'GA1.3.2065482246.1651487879',
        '_fbp': 'fb.2.1651487879006.854201146',
        '__gads': 'ID=293401b0ae4479e9-2250976589d20099:T=1651487879:RT=1651487879:S=ALNI_MZ_oVdweVxKkRrx9a57H3W4jvqWYg',
        '_gcl_aw': 'GCL.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB',
        '_gac_UA-72680702-5': '1.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB',
        'locale': 'ko',
        'tracking_id': 'd463de06-3f3e-4d6c-a24e-b07c3ed4ba2f',
        '_gid': 'GA1.3.420749075.1653374750',
        '__gpi': 'UID=0000059ef05c1610:T=1653132258:RT=1653374752:S=ALNI_MZzI8JE0uS7e2OgikIbXIIRpk4CEQ',
        '_beu_utm_source': '__null__',
        '_beu_utm_medium': '__null__',
        '_beu_utm_campaign': '__null__',
        '_beu_utm_term': '__null__',
        '_beu_utm_content': '__null__',
        '_rtetSessId': 'mDQbh2e63',
        '_clck': 'd6s3xo|1|f1q|0',
        '_gat_UA-72680702-5': '1',
        '_rtetSessPageSeq': '3',
        '_clsk': '7fcjot|1653376460627|22|1|f.clarity.ms/collect',
    }

    headers = {
        'authority': 'programmers.co.kr',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_programmers_session_production=8afb764fc54ea3576ad07db48d3c723c; _gcl_au=1.1.1544457234.1651487879; _ga=GA1.3.2065482246.1651487879; _fbp=fb.2.1651487879006.854201146; __gads=ID=293401b0ae4479e9-2250976589d20099:T=1651487879:RT=1651487879:S=ALNI_MZ_oVdweVxKkRrx9a57H3W4jvqWYg; _gcl_aw=GCL.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB; _gac_UA-72680702-5=1.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB; locale=ko; tracking_id=d463de06-3f3e-4d6c-a24e-b07c3ed4ba2f; _gid=GA1.3.420749075.1653374750; __gpi=UID=0000059ef05c1610:T=1653132258:RT=1653374752:S=ALNI_MZzI8JE0uS7e2OgikIbXIIRpk4CEQ; _beu_utm_source=__null__; _beu_utm_medium=__null__; _beu_utm_campaign=__null__; _beu_utm_term=__null__; _beu_utm_content=__null__; _rtetSessId=mDQbh2e63; _clck=d6s3xo|1|f1q|0; _gat_UA-72680702-5=1; _rtetSessPageSeq=3; _clsk=7fcjot|1653376460627|22|1|f.clarity.ms/collect',
        'referer': 'https://programmers.co.kr/job_positions/'+str(id)+'?by_theme=true',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '5386872d4e0e46288547c6209ff923c0-bd63009db8e2024a-0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    params = {
        'by_theme': 'true',
    }

    response = requests.get('https://programmers.co.kr/api/job_positions/'+str(id), params=params, cookies=cookies, headers=headers)
    html = response.text
    dict = json.loads(html)
    df = json_normalize(dict['jobPosition'])
    dday = df['period'].values[0]
    try:
        dday = dday.split(' ')[3]
        year, month, day = dday.split('.')
        dday = year+'. '+month+'. '+day
        pr_dday.append(dday)
    except:
        pr_dday.append(dday)


# In[33]:


for i in range(len(pr_titles)):
    li_tmp = {"title": pr_titles[i], "dday": pr_dday[i], "link": pr_links[i], "기업": pr_company[i]}
    job.append(li_tmp)

with open('취업.json', 'w', encoding="utf-8") as make_file: 
    json.dump(job, make_file, ensure_ascii = False, indent="\t")

