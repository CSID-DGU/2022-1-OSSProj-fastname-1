#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd
from pandas import json_normalize
import numpy as np

import requests
import json
from bs4 import BeautifulSoup
import re
import ssl
import datetime
from datetime import date, timedelta
from dateutil.parser import parse
from urllib.request import urlopen
context=ssl._create_unverified_context()


# In[35]:


links = []
titles = []
insts = []
end_list = []
tags = []

# 잡코리아
base_url = 'http://www.jobkorea.co.kr'

url= 'https://www.jobkorea.co.kr/starter/?chkSubmit=1&schCareer=&schLocal=&schPart=10016&schMajor=&schEduLevel=5&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt='
headers = {'User-Agent': 'Mozilla/5.0'} 
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), 'html.parser')
element_num = len(soup.select(' .tit > .link > span'))
cnt = int(soup.select(' #TabIngCount')[0].text.replace('(', '').replace(')', '').replace(',', ''))
if cnt % element_num == 0:
    page_num = int(cnt / element_num)
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
        tag = soup.select(' .sTit')[i].text.replace('', '').split('\n')
        tag = list(filter(None, tag))
        tags.append(tag)
        dday = (soup.select(' .side > .day')[i].text).replace("~", "")
        dday = dday.split('(')[0]
        try:
            year, month, day = dday.split('.')
            dday = year+'. '+month+'. '+day
        except:
            end_list.append(dday)
        end_list.append(dday)


# In[36]:


job = []

for i in range(len(titles)):
    li_tmp = {"title": titles[i], "dday": end_list[i], "link": links[i], "기업": insts[i], '태그': tags[i]}
    job.append(li_tmp)


# In[37]:


# 취업 프로그래머스

cookies = {
    '_programmers_session_production': '8afb764fc54ea3576ad07db48d3c723c',
    '_gcl_au': '1.1.1544457234.1651487879',
    '_ga': 'GA1.3.2065482246.1651487879',
    '_fbp': 'fb.2.1651487879006.854201146',
    '__gads': 'ID=293401b0ae4479e9-2250976589d20099:T=1651487879:RT=1651487879:S=ALNI_MZ_oVdweVxKkRrx9a57H3W4jvqWYg',
    '_gcl_aw': 'GCL.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB',
    '_gac_UA-72680702-5': '1.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB',
    '_gid': 'GA1.3.292899406.1653555806',
    'locale': 'ko',
    '_gat_UA-72680702-5': '1',
    '__gpi': 'UID=0000059ef05c1610:T=1653132258:RT=1653627014:S=ALNI_MZzI8JE0uS7e2OgikIbXIIRpk4CEQ',
    '_beu_utm_source': '__null__',
    '_beu_utm_medium': '__null__',
    '_beu_utm_campaign': '__null__',
    '_beu_utm_term': '__null__',
    '_beu_utm_content': '__null__',
    '_rtetSessId': 'XL7rm7e61',
    '_rtetSessPageSeq': '0',
    '_clck': 'd6s3xo|1|f1t|0',
    '_clsk': 'xmkdjc|1653627017727|1|1|f.clarity.ms/collect',
}

headers = {
    'authority': 'programmers.co.kr',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_programmers_session_production=8afb764fc54ea3576ad07db48d3c723c; _gcl_au=1.1.1544457234.1651487879; _ga=GA1.3.2065482246.1651487879; _fbp=fb.2.1651487879006.854201146; __gads=ID=293401b0ae4479e9-2250976589d20099:T=1651487879:RT=1651487879:S=ALNI_MZ_oVdweVxKkRrx9a57H3W4jvqWYg; _gcl_aw=GCL.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB; _gac_UA-72680702-5=1.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB; _gid=GA1.3.292899406.1653555806; locale=ko; _gat_UA-72680702-5=1; __gpi=UID=0000059ef05c1610:T=1653132258:RT=1653627014:S=ALNI_MZzI8JE0uS7e2OgikIbXIIRpk4CEQ; _beu_utm_source=__null__; _beu_utm_medium=__null__; _beu_utm_campaign=__null__; _beu_utm_term=__null__; _beu_utm_content=__null__; _rtetSessId=XL7rm7e61; _rtetSessPageSeq=0; _clck=d6s3xo|1|f1t|0; _clsk=xmkdjc|1653627017727|1|1|f.clarity.ms/collect',
    'referer': 'https://programmers.co.kr/job',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'fe279517b06f43329aada5c3b4a6d6a2-b7cb1d610718a65f-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
}

response = requests.get('https://programmers.co.kr/api/job_positions/job_categories', cookies=cookies, headers=headers)
html = response.text
dict = json.loads(html)
tag_df = json_normalize(dict) # id 코드


# In[38]:


pr_titles = []
pr_company = []
pr_links = []
pr_dday = []
pr_tags = []

for i in range(1, 27):
    cookies = {
        '_programmers_session_production': '8afb764fc54ea3576ad07db48d3c723c',
        '_gcl_au': '1.1.1544457234.1651487879',
        '_ga': 'GA1.3.2065482246.1651487879',
        '_fbp': 'fb.2.1651487879006.854201146',
        '__gads': 'ID=293401b0ae4479e9-2250976589d20099:T=1651487879:RT=1651487879:S=ALNI_MZ_oVdweVxKkRrx9a57H3W4jvqWYg',
        '_gcl_aw': 'GCL.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB',
        '_gac_UA-72680702-5': '1.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB',
        'locale': 'ko',
        '_gid': 'GA1.3.292899406.1653555806',
        '_gat_UA-72680702-5': '1',
        'tracking_id': '696c7313-5f9e-4b69-9dd3-f22feea8ee42',
        '__gpi': 'UID=0000059ef05c1610:T=1653132258:RT=1653555807:S=ALNI_MZzI8JE0uS7e2OgikIbXIIRpk4CEQ',
        '_beu_utm_source': '__null__',
        '_beu_utm_medium': '__null__',
        '_beu_utm_campaign': '__null__',
        '_beu_utm_term': '__null__',
        '_beu_utm_content': '__null__',
        '_rtetSessId': 'hzroY7Y87',
        '_rtetSessPageSeq': '0',
        '_clck': 'd6s3xo|1|f1s|0',
        '_clsk': '1distji|1653555821857|3|1|f.clarity.ms/collect',
    }

    headers = {
        'authority': 'programmers.co.kr',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_programmers_session_production=8afb764fc54ea3576ad07db48d3c723c; _gcl_au=1.1.1544457234.1651487879; _ga=GA1.3.2065482246.1651487879; _fbp=fb.2.1651487879006.854201146; __gads=ID=293401b0ae4479e9-2250976589d20099:T=1651487879:RT=1651487879:S=ALNI_MZ_oVdweVxKkRrx9a57H3W4jvqWYg; _gcl_aw=GCL.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB; _gac_UA-72680702-5=1.1653132257.Cj0KCQjwm6KUBhC3ARIsACIwxBjSWdq9VSzsdmXrw88JQKTxsmyqwcgERGy3IZPdCv3chKkEiRXiKgQaAlzNEALw_wcB; locale=ko; _gid=GA1.3.292899406.1653555806; _gat_UA-72680702-5=1; tracking_id=696c7313-5f9e-4b69-9dd3-f22feea8ee42; __gpi=UID=0000059ef05c1610:T=1653132258:RT=1653555807:S=ALNI_MZzI8JE0uS7e2OgikIbXIIRpk4CEQ; _beu_utm_source=__null__; _beu_utm_medium=__null__; _beu_utm_campaign=__null__; _beu_utm_term=__null__; _beu_utm_content=__null__; _rtetSessId=hzroY7Y87; _rtetSessPageSeq=0; _clck=d6s3xo|1|f1s|0; _clsk=1distji|1653555821857|3|1|f.clarity.ms/collect',
        'referer': 'https://programmers.co.kr/job?page='+str(i)+'&order=recent',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': 'dbeada50559a4a27a21f0bfd6b9b926a-b581ce68638e55f3-0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    params = {
        'order': 'recent',
        'page': str(i),
    }

    response = requests.get('https://programmers.co.kr/api/job_positions', params=params, cookies=cookies, headers=headers)

    html = response.text
    dict = json.loads(html)
    df = json_normalize(dict['jobPositions'])
    df = df.drop(['careerRange', 'companyId', 'jobType', 'maxSalary', 'minSalary', 'personalized', 'signingBonus', 'company.revenue', 'company.hideRevenue', 'company.blog', 'company.funding', 'company.hideFunding', 'company.countryCode', 'careerOption', 'createdAt',
    'career', 'startAt', 'updatedAt', 'company.serviceUrl' ,'company.logoUrl' ,'company.employees', 'company.developers', 'company.employeesCount', 'company.averageResponseTime', 'company.id', 'status', 'company.serviceName', 'company.homeUrl', 'company.address', 'id', 'period', 'technicalTags',
    'company.benefitTags', 'teamTechnicalTags'], axis=1)

    df = df[['title', 'company.name', 'url', 'address', 'jobCategoryIds']]
    
    for j in range(len(df)):
        title = df.iloc[j][0]
        name = df.iloc[j][1]
        link = df.iloc[j][2]
        link = 'https://programmers.co.kr'+str(link)
        pr_titles.append(title)
        pr_company.append(name)
        pr_links.append(link)

    for l in range(0, 20):
        tmp = []
        tag = str(df.iloc[l, 4]).replace('[', '').replace(']', '')
        tag = tag.split(', ')
        for m in tag:
            if m == '':
                tmp.append('추가필요')
            else:
                m = int(m)
                id = tag_df.loc[tag_df['id'] == m].iloc[0, 1]
                tmp.append(id)  # ['안드로이드 앱']
                                # ['데브옵스']
                                # ['프론트엔드', '웹 풀스택']
        pr_tags.append(tmp)


# In[39]:


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
    df2 = json_normalize(dict['jobPosition'])
    dday = df2['period'].values[0]
    if '채용' in dday:
        pr_dday.append(dday)
    else:
        dday = dday.split(' ')[3]
        year, month, day = dday.split('-')
        dday = year+'. '+month+'. '+day
        pr_dday.append(dday)


# In[40]:


for li in pr_links:
    li = li.split('/')[-1]
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
        'referer': 'https://programmers.co.kr/job_positions/'+li+'?by_theme=true',
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

    response = requests.get('https://programmers.co.kr/api/job_positions/'+li, params=params, cookies=cookies, headers=headers)
    html = response.text
    dict = json.loads(html)
    df3 = json_normalize(dict['jobPosition'])
    df3 = df3.drop(['address', 'career', 'careerRange', 'companyId', 'jobType', 'maxSalary', 'minSalary', 'personalized', 'signingBonus', 'company.employeesCount', 'company.logoUrl', 'company.developers', 'company.employees', 'startAt', 'createdAt', 'updatedAt', 'careerOption', 'period', 'company.serviceUrl', 'teamTechnicalTags', 'countryCode', 'latitude', 'longitude',
        'company.serviceName', 'company.homeUrl', 'company.funding', 'company.hideFunding'], axis=1)
    technicalTags = df3.iloc[0, 4] # 행 열
    id = df3.iloc[0, 0]

    link = 'https://programmers.co.kr/job_positions/'+str(id)
    num = int(pr_links.index(link))
    tmp = []
    for li in technicalTags:
        li = li['name']
        tmp.append(li)
    pr_tags[num] = pr_tags[num] + tmp
    


# In[41]:


for i in range(len(pr_titles)):
    li_tmp = {"title": pr_titles[i], "dday": pr_dday[i], "link": pr_links[i], "기업": pr_company[i], '태그': pr_tags[i]}
    job.append(li_tmp)

titles = []
ddays = []
links = []
companies = []
tags = []
new_tags = []
check_app = ['iOS', '앱', '게임', '소프트웨어', '응용', '어플리케이션', '아이폰', '안드로이드']
check_AI = ['AI', 'IoT', '러닝', '인공지능']
check_web = ['웹', '엔드', 'HTML', 'web']
check_data = ['데이터', 'DB','Data']
check_server = ['서버', '블록체인', '보안']
check_system = ['Unix', 'Linux', '임베디드','시스템']

df = pd.DataFrame(job)
df = df.sort_values(by=['dday'])

for i in range(len(df)):
        ttag = []
        title = df.iloc[i][0]
        dday = df.iloc[i][1]
        link = df.iloc[i][2]
        company = df.iloc[i][3]
        tag = df.iloc[i][4]
        for k in tag:
            if any(word in k for word in check_app):        
                ttag.append('응용')
            if any(word in k for word in check_AI):         
                ttag.append('인공지능')
            if any(word in k for word in check_web):       
                ttag.append('웹')
            if any(word in k for word in check_data):      
                ttag.append('데이터')
            if any(word in k for word in check_server):
                ttag.append('서버')
            if any(word in k for word in check_system):
                ttag.append('시스템')
        if len(ttag) == 0:
            ttag.append('기타')
        result = set(ttag)
        ttag = list(result)
        titles.append(title)
        ddays.append(dday)
        links.append(link)
        companies.append(company)
        tags.append(tag)
        new_tags.append(ttag)

job = []

for i in range(len(titles)):
    li_tmp = {"title": titles[i], "dday": ddays[i], "link": links[i], "기업": companies[i], '태그': tags[i], "bigtag":new_tags[i]}
    job.append(li_tmp)

with open('../json 결과/취업.json', 'w', encoding="utf-8") as make_file: 
    json.dump(job, make_file, ensure_ascii = False, indent="\t")
