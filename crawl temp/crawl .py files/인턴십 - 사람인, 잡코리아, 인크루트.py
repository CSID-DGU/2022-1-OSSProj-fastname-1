#!/usr/bin/env python
# coding: utf-8

# In[47]:


import pandas as pd
from pandas import json_normalize
import numpy as np
from bs4 import BeautifulSoup
import re
import urllib.request
from urllib.request import urlopen
import ssl
from dateutil.parser import parse
import json
import requests
from datetime import datetime
context=ssl._create_unverified_context()


# In[48]:


# title, company, link, tag, dday
# 사람인
titles = []
ddays = []
links = []
companies = []
tags = []

for i in range(1, 10):
    cookies = {
        'PCID': '16519199768421417985089',
        '_gcl_au': '1.1.907707392.1651919977',
        '__gads': 'ID=ab02132b4e2dc7db:T=1651919977:S=ALNI_MYSYOO_0DXBZtEYCph0ex5kzWGt2A',
        '_gaexp': 'GAX1.3.TPhZbu4VR1m24zFMhnHzpA.19221.1',
        '_gid': 'GA1.3.763058907.1653127172',
        'PHPSESSID': '8jd9d80f5obtnuttf14o90chpihbujnbl14qccrqr28v048h9j',
        'session_cookie': 'QCHlt.1948432442 | undefined | undefined | undefined | undefined |  | Sun May 22 2022 09:24:25 GMT+0900',
        '__gpi': 'UID=000005335141bee3:T=1651919977:RT=1653179622:S=ALNI_Mb9pUJdE0RJ6o1OxPfs1K_lTC2W9A',
        'mkt_ecommerce_pagepath': '/zf_user/jobs/list/domestic',
        'RSRVID': 'web26|YomJE|YomCu',
        '_ga_GR2XRGQ0FK': 'GS1.1.1653179065.5.1.1653180686.60',
        '_gat': '1',
        'wcs_bt': 's_1d3a45fb0bfe:1653180686',
        '_rc': 'https://www.saramin.co.kr/zf_user/jobs/list/domestic?page=2&loc_mcd=101000&ind_cd=302%2C305%2C306%2C308%2C301&job_type=4&search_optional_item=y&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=domestic&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=3',
        '_ga': 'GA1.3.283320388.1651919977',
        '_gat_UA-12546634-1': '1',
        '_gali': 'job_type_4',
        '_gat_UA-12546634-15': '1',
        '_gat_UA-12546634-22': '1',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'PCID=16519199768421417985089; _gcl_au=1.1.907707392.1651919977; __gads=ID=ab02132b4e2dc7db:T=1651919977:S=ALNI_MYSYOO_0DXBZtEYCph0ex5kzWGt2A; _gaexp=GAX1.3.TPhZbu4VR1m24zFMhnHzpA.19221.1; _gid=GA1.3.763058907.1653127172; PHPSESSID=8jd9d80f5obtnuttf14o90chpihbujnbl14qccrqr28v048h9j; session_cookie=QCHlt.1948432442 | undefined | undefined | undefined | undefined |  | Sun May 22 2022 09:24:25 GMT+0900; __gpi=UID=000005335141bee3:T=1651919977:RT=1653179622:S=ALNI_Mb9pUJdE0RJ6o1OxPfs1K_lTC2W9A; mkt_ecommerce_pagepath=/zf_user/jobs/list/domestic; RSRVID=web26|YomJE|YomCu; _ga_GR2XRGQ0FK=GS1.1.1653179065.5.1.1653180686.60; _gat=1; wcs_bt=s_1d3a45fb0bfe:1653180686; _rc=https://www.saramin.co.kr/zf_user/jobs/list/domestic?page=2&loc_mcd=101000&ind_cd=302%2C305%2C306%2C308%2C301&job_type=4&search_optional_item=y&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=domestic&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=3; _ga=GA1.3.283320388.1651919977; _gat_UA-12546634-1=1; _gali=job_type_4; _gat_UA-12546634-15=1; _gat_UA-12546634-22=1',
        'Referer': 'https://www.saramin.co.kr/zf_user/jobs/list/domestic?page=1&loc_mcd=101000&ind_cd=302%2C305%2C306%2C308%2C301&job_type=4&search_optional_item=y&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=domestic&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=3',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'page': str(i),
        'loc_mcd': '101000',
        'ind_cd': '302,305,306,308,301',
        'job_type': '4',
        'search_optional_item': 'y',
        'search_done': 'y',
        'panel_count': 'y',
        'isAjaxRequest': '0',
        'page_count': '50',
        'sort': 'RL',
        'type': 'domestic',
        'is_param': '1',
        'isSearchResultEmpty': '1',
        'isSectionHome': '0',
        'searchParamCount': '3',
    }

    response = requests.get('https://www.saramin.co.kr/zf_user/jobs/list/domestic', params=params, cookies=cookies, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    #pagenum = len(soup.select('div.pagination > a'))

    for j in range(0, 50):
        try:
            tag = []
            day = ["상시채용", "오늘마감", "채용시", "내일마감"]
            title = soup.select('a.str_tit')[j*2+1].text
            company = soup.select('a.str_tit')[j*2].text
            dday = soup.select('p.deadlines')[j].text.replace('~', '').lstrip().split('(')[0].replace('/', '. ').rstrip()
            if dday not in day:
                dday = '2022. ' + dday
            else:
                dday = dday            
            link = soup.select('a.str_tit')[j*2]['href']
            link = link.split('=')[-1]
            tag_list = soup.select('.job_meta > span.job_sector')[j]
            tag_num = len(tag_list.select('span'))
            for k in range(tag_num):
                temp = tag_list.select('span')[k].text
                tag.append(temp)
            #자료 저장
            titles.append(title)
            ddays.append(dday)
            links.append('https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx='+str(link)+'&recommend_ids=eJxNT7kVw1AImyY94qbOINl%2Fi%2BB8E1zq6Vah4CR8kusVbxUSFqWGuCCXRFWzwGGVxGzEnBbmOixXIFlXjCjhf5QnSnNYsoJXrFetruQbZjs5dlVm%2FIr8XmUG2yLvIfyAYdhVCe1Z25vC1QdBRxwuiueFw86FSf4CQ%2FlABQ%3D%3D&view_type=list&gz=1&t_ref_content=general&t_ref=area_recruit#seq=0')
            companies.append(company)
            tags.append(tag)
        except:
            break


# In[49]:


intern = []

for i in range(len(titles)):
    li_tmp = {"title": titles[i], "dday": ddays[i], "link": links[i], "company": companies[i], "tag": tags[i]}
    intern.append(li_tmp)


# In[50]:


# 인크루트
# title, company, link, tag, dday
titles = []
ddays = []
links = []
companies = []
tags = []

url = 'https://job.incruit.com/jobdb_list/searchjob.asp?occ1=150&jobty=4&page=1'
req = urllib.request.urlopen(url)
res = req.read()
soup = BeautifulSoup(res,'html.parser')
page_num = len(soup.select('#JobList_Area > div:nth-child(2) > p > a'))
today_month = datetime.today().month
today_day = datetime.today().day

for i in range (1, page_num+1):
    url = 'https://job.incruit.com/jobdb_list/searchjob.asp?occ1=150&jobty=4&page='+str(i)
    req = urllib.request.urlopen(url)
    res = req.read()
    soup = BeautifulSoup(res,'html.parser')
    
    for j in range(0, 60):
        #JobList_Area > div:nth-child(2) > div.cBbslist_contenst > ul:nth-child(1) > li > div.cell_mid > div.cl_top > a
        #JobList_Area > div:nth-child(2) > div.cBbslist_contenst > ul:nth-child(1) > li > div.cell_first > div.cl_top > a
        try:
            title = soup.select('.cl_top > a')[j*2+ 1].text
            link = soup.select('.cl_top > a')[j*2+ 1]['href']  
            company = soup.select('.cl_top > a')[j*2].text
            tag = soup.select('.cl_btm')[j*3 + 1].text.replace('\n', '')
            tag = tag.split(', ')
            dday = soup.select('.cl_btm')[j*3 + 2].text
            if '채용시' in dday or '마감' in dday:
                dday = dday.split('(')[0]
            if '상시' in dday:
                dday = '상시채용'
            else:
                dday = dday.replace('~', '').split(' ')[0]
                month, day = dday.split('.')
                month = int(month)
                day = int(day)
                if month < today_month:
                    dday = '2023. '+ '0'+ str(month) +'. '+str(day)
                else:
                    dday = '2022. '+ '0'+ str(month) +'. '+str(day)

        except:
            break
        titles.append(title)
        ddays.append(dday)
        links.append(link)
        companies.append(company)
        tags.append(tag)

for i in range(len(titles)):
    li_tmp = li_tmp = {"title": titles[i], "dday": ddays[i], "link": links[i], "company": companies[i], "tag": tags[i]}
    intern.append(li_tmp)


# In[51]:


# 잡코리아
# title, company, link, tag, dday
titles = []
ddays = []
links = []
companies = []
tags = []

for i in range(1, 10):
    cookies = {
        'CookieNo': '1610920874',
        'PCID': '16514845459050250101676',
        '__gads': 'ID=c336a58349a51c0e-2281924b88d20005:T=1651484623:RT=1651484623:S=ALNI_Mb-0-OeaFhqwNGo5Uo8CEWEYmUeSg',
        '_ga': 'GA1.3.1481820761.1651484623',
        'mainContents': '0',
        '_fbp': 'fb.2.1651484624285.1762510709',
        'JKStarter': '',
        'ab.storage.deviceId.b9795c74-cdce-4881-a000-eb185c0d072e': '%7B%22g%22%3A%222aecf1db-27d0-3ca0-0816-540a432606d9%22%2C%22c%22%3A1651722470528%2C%22l%22%3A1651722470528%7D',
        'DirectStat': 'ON',
        '_wp_uid': '2-3ff6b48488afe6324baa5c30abaa9ddf-s1650376346.246000|windows_10|chrome-1fd9cv0',
        '_gcl_au': '1.1.947439924.1652351093',
        'G_ENABLED_IDPS': 'google',
        'PositionOfferLayerView': '1',
        'smenu': 'menu%5Fortgi=20220510/121717&menu%5Fpassassay=20220512/192808',
        'StarterRecentMenu': 'Recent0=14&Recent1=16&Recent2=1',
        'ab.storage.sessionId.b9795c74-cdce-4881-a000-eb185c0d072e': '%7B%22g%22%3A%223566b424-e135-e931-e074-28681e6c483e%22%2C%22e%22%3A1652353211045%2C%22c%22%3A1652351197789%2C%22l%22%3A1652351411045%7D',
        '_gac_UA-34423025-1': '1.1652351423.Cj0KCQjw4PKTBhD8ARIsAHChzRIDFn2p44qx4_duBc6xoh_OWVQcTHtJi0CTh4zYYhN6y6MBnKYASuwaAu0_EALw_wcB',
        'GoodJobMenu': 'menu%5Fform=20220513/172503',
        'TR10148105490_t_pa2': '3.460.693.0.336d5ebc5436534e61d16e63ddfca327.d36df91c3a7baa057f8388f1d6c3acda.null.0',
        'recentKeyword': '%5B%22%uC778%uD134%20%uACF5%uACE0%20%uC0AC%uC774%uD2B8%22%2C%22%uC778%uD134%22%5D',
        'DSIF': 'pmax',
        '_gac_UA-75522609-1': '1.1653127095.Cj0KCQjwm6KUBhC3ARIsACIwxBhJ0a9oMIBNcYOy7i2Mf1KBPbHiAI0MLsMbyssvK2ST9dfYN9P9hgMaAu-eEALw_wcB',
        'TR10148105490_t_pa1': '3.460.693.0.336d5ebc5436534e61d16e63ddfca327.c63ff26fb5a8766433a6f32007425820.null.14495127078892140',
        '_gcl_aw': 'GCL.1653383426.Cj0KCQjwhLKUBhDiARIsAMaTLnFA9gi7jg7pDZkHv-uQKjVBIMDXXTDOXGEyiUEun6TltQyuwyvv7c8aAofREALw_wcB',
        '_gac_UA-213826050-3': '1.1653383427.Cj0KCQjwhLKUBhDiARIsAMaTLnFA9gi7jg7pDZkHv-uQKjVBIMDXXTDOXGEyiUEun6TltQyuwyvv7c8aAofREALw_wcB',
        'ASP.NET_SessionId': 'bpiduialf4yuuozcc0shlw0k',
        'jobkorea': 'Site_Oem_Code=C1',
        'GTMVars': '63787639f127dd435acf409c37584ef6',
        'GTMVarsFrom': 'NET:13:51:40',
        'ECHO_SESSION': '8521653540702226',
        '__gpi': 'UID=0000052bedb811d6:T=1651741632:RT=1653540704:S=ALNI_MbKD-W4EtxZ9E0SDjy5ppkfjxGQxg',
        '_gid': 'GA1.3.693575665.1653540704',
        'MainRcntlyData': '%3c%6c%69%3e%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%68%6f%6d%65%22%3e%c3%a4%bf%eb%c1%a4%ba%b8%3c%2f%61%3e%20%26%67%74%3b%20%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%6a%6f%62%6c%69%73%74%3f%6d%65%6e%75%63%6f%64%65%3d%6c%6f%63%61%6c%26%6c%6f%63%61%6c%6f%72%64%65%72%3d%31%22%20%63%6c%61%73%73%3d%22%63%61%74%65%22%3e%c1%f6%bf%aa%ba%b0%3c%2f%61%3e%3c%2f%6c%69%3e%7c%24%24%7c%3c%6c%69%3e%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%68%6f%6d%65%22%3e%c3%a4%bf%eb%c1%a4%ba%b8%3c%2f%61%3e%20%26%67%74%3b%20%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%6a%6f%62%6c%69%73%74%3f%6d%65%6e%75%63%6f%64%65%3d%64%75%74%79%22%20%63%6c%61%73%73%3d%22%63%61%74%65%22%3e%c1%f7%b9%ab%ba%b0%3c%2f%61%3e%3c%2f%6c%69%3e%7c%24%24%7c%3c%6c%69%3e%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%6a%6f%62%6c%69%73%74%3f%6d%65%6e%75%63%6f%64%65%3d%64%75%74%79%22%3e%c1%f7%b9%ab%ba%b0%3c%2f%61%3e%20%26%67%74%3b%20%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%6a%6f%62%6c%69%73%74%3f%6d%65%6e%75%63%6f%64%65%3d%64%75%74%79%26%64%75%74%79%43%74%67%72%3d%31%30%30%31%36%22%20%63%6c%61%73%73%3d%22%63%61%74%65%22%3e%49%54%a1%a4%c0%ce%c5%cd%b3%dd%3c%2f%61%3e%3c%2f%6c%69%3e%7c%24%24%7c',
        'Main_Top_Banner_Seq': '1',
        'TR10148105490_t_uid': '14495555018140948.1653540706054',
        'TR10148105490_t_sst': '14495539400001140.1653540706054',
        'TR10148105490_t_if': '15.0.0.0.null.null.null.0',
        'cto_bundle': 'okytUF9rciUyRkxnckFSVk1xZmVPSUQ4JTJCTjJ3OGhGWCUyRiUyRjhZZnlmcFRLJTJCSEJZQVQ1bURzNUtDQWVIMXlJaDgyS3ZLJTJCZ1VWdlNHd1RtdnZYSVliMHpOTVFoV2h2Q0N1NmZpcldnaSUyQlhNNjBwMnclMkJ5dmtNQlZDZ1dmRm92SHNrRDJSdUZtV3dka2o5QUhXY1o4N0klMkJ3dVptVHdpUnclM0QlM0Q',
        'RSCondition': '[{"CookieIndex":"20220526135436","Cndt_No":0,"M_Id":"","Jobtype_Code":"1000100,1000101,1000102,1000096,1000097,1000104,1000094,1000109,1000110","Employ_Type":"3","Reg_Dt":"2022-05-26T13:54:36.4912113+09:00","IsKeep":true},{"CookieIndex":"20220526135150","Cndt_No":0,"M_Id":"","Employ_Type":"3","Reg_Dt":"2022-05-26T13:51:50.8033792+09:00","IsKeep":true},{"CookieIndex":"20220524181321","Cndt_No":0,"M_Id":"","Jobtype_Code":"1000101,1000102,1000096,1000098,1000104,1000105,1000094,1000109,1000097,1000100","Edu_Level":"5","Employ_Type":"3","Reg_Dt":"2022-05-24T18:13:21.808864+09:00","IsKeep":true},{"CookieIndex":"20220524181246","Cndt_No":0,"M_Id":"","Jobtype_Code":"1000101,1000102,1000096,1000098,1000104,1000105,1000094,1000109,1000100,1000097","Edu_Level":"5","Employ_Type":"3","Reg_Dt":"2022-05-24T18:12:46.2932003+09:00","IsKeep":true},{"CookieIndex":"20220524181213","Cndt_No":0,"M_Id":"","Jobtype_Code":"1000101,1000102,1000096,1000097,1000098,1000104,1000105,1000094,1000109,1000100","Edu_Level":"5","Employ_Type":"3","Reg_Dt":"2022-05-24T18:12:13.0879047+09:00","IsKeep":true}]',
    }

    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'CookieNo=1610920874; PCID=16514845459050250101676; __gads=ID=c336a58349a51c0e-2281924b88d20005:T=1651484623:RT=1651484623:S=ALNI_Mb-0-OeaFhqwNGo5Uo8CEWEYmUeSg; _ga=GA1.3.1481820761.1651484623; mainContents=0; _fbp=fb.2.1651484624285.1762510709; JKStarter=; ab.storage.deviceId.b9795c74-cdce-4881-a000-eb185c0d072e=%7B%22g%22%3A%222aecf1db-27d0-3ca0-0816-540a432606d9%22%2C%22c%22%3A1651722470528%2C%22l%22%3A1651722470528%7D; DirectStat=ON; _wp_uid=2-3ff6b48488afe6324baa5c30abaa9ddf-s1650376346.246000|windows_10|chrome-1fd9cv0; _gcl_au=1.1.947439924.1652351093; G_ENABLED_IDPS=google; PositionOfferLayerView=1; smenu=menu%5Fortgi=20220510/121717&menu%5Fpassassay=20220512/192808; StarterRecentMenu=Recent0=14&Recent1=16&Recent2=1; ab.storage.sessionId.b9795c74-cdce-4881-a000-eb185c0d072e=%7B%22g%22%3A%223566b424-e135-e931-e074-28681e6c483e%22%2C%22e%22%3A1652353211045%2C%22c%22%3A1652351197789%2C%22l%22%3A1652351411045%7D; _gac_UA-34423025-1=1.1652351423.Cj0KCQjw4PKTBhD8ARIsAHChzRIDFn2p44qx4_duBc6xoh_OWVQcTHtJi0CTh4zYYhN6y6MBnKYASuwaAu0_EALw_wcB; GoodJobMenu=menu%5Fform=20220513/172503; TR10148105490_t_pa2=3.460.693.0.336d5ebc5436534e61d16e63ddfca327.d36df91c3a7baa057f8388f1d6c3acda.null.0; recentKeyword=%5B%22%uC778%uD134%20%uACF5%uACE0%20%uC0AC%uC774%uD2B8%22%2C%22%uC778%uD134%22%5D; DSIF=pmax; _gac_UA-75522609-1=1.1653127095.Cj0KCQjwm6KUBhC3ARIsACIwxBhJ0a9oMIBNcYOy7i2Mf1KBPbHiAI0MLsMbyssvK2ST9dfYN9P9hgMaAu-eEALw_wcB; TR10148105490_t_pa1=3.460.693.0.336d5ebc5436534e61d16e63ddfca327.c63ff26fb5a8766433a6f32007425820.null.14495127078892140; _gcl_aw=GCL.1653383426.Cj0KCQjwhLKUBhDiARIsAMaTLnFA9gi7jg7pDZkHv-uQKjVBIMDXXTDOXGEyiUEun6TltQyuwyvv7c8aAofREALw_wcB; _gac_UA-213826050-3=1.1653383427.Cj0KCQjwhLKUBhDiARIsAMaTLnFA9gi7jg7pDZkHv-uQKjVBIMDXXTDOXGEyiUEun6TltQyuwyvv7c8aAofREALw_wcB; ASP.NET_SessionId=bpiduialf4yuuozcc0shlw0k; jobkorea=Site_Oem_Code=C1; GTMVars=63787639f127dd435acf409c37584ef6; GTMVarsFrom=NET:13:51:40; ECHO_SESSION=8521653540702226; __gpi=UID=0000052bedb811d6:T=1651741632:RT=1653540704:S=ALNI_MbKD-W4EtxZ9E0SDjy5ppkfjxGQxg; _gid=GA1.3.693575665.1653540704; MainRcntlyData=%3c%6c%69%3e%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%68%6f%6d%65%22%3e%c3%a4%bf%eb%c1%a4%ba%b8%3c%2f%61%3e%20%26%67%74%3b%20%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%6a%6f%62%6c%69%73%74%3f%6d%65%6e%75%63%6f%64%65%3d%6c%6f%63%61%6c%26%6c%6f%63%61%6c%6f%72%64%65%72%3d%31%22%20%63%6c%61%73%73%3d%22%63%61%74%65%22%3e%c1%f6%bf%aa%ba%b0%3c%2f%61%3e%3c%2f%6c%69%3e%7c%24%24%7c%3c%6c%69%3e%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%68%6f%6d%65%22%3e%c3%a4%bf%eb%c1%a4%ba%b8%3c%2f%61%3e%20%26%67%74%3b%20%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%6a%6f%62%6c%69%73%74%3f%6d%65%6e%75%63%6f%64%65%3d%64%75%74%79%22%20%63%6c%61%73%73%3d%22%63%61%74%65%22%3e%c1%f7%b9%ab%ba%b0%3c%2f%61%3e%3c%2f%6c%69%3e%7c%24%24%7c%3c%6c%69%3e%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%6a%6f%62%6c%69%73%74%3f%6d%65%6e%75%63%6f%64%65%3d%64%75%74%79%22%3e%c1%f7%b9%ab%ba%b0%3c%2f%61%3e%20%26%67%74%3b%20%3c%61%20%68%72%65%66%3d%22%2f%72%65%63%72%75%69%74%2f%6a%6f%62%6c%69%73%74%3f%6d%65%6e%75%63%6f%64%65%3d%64%75%74%79%26%64%75%74%79%43%74%67%72%3d%31%30%30%31%36%22%20%63%6c%61%73%73%3d%22%63%61%74%65%22%3e%49%54%a1%a4%c0%ce%c5%cd%b3%dd%3c%2f%61%3e%3c%2f%6c%69%3e%7c%24%24%7c; Main_Top_Banner_Seq=1; TR10148105490_t_uid=14495555018140948.1653540706054; TR10148105490_t_sst=14495539400001140.1653540706054; TR10148105490_t_if=15.0.0.0.null.null.null.0; cto_bundle=okytUF9rciUyRkxnckFSVk1xZmVPSUQ4JTJCTjJ3OGhGWCUyRiUyRjhZZnlmcFRLJTJCSEJZQVQ1bURzNUtDQWVIMXlJaDgyS3ZLJTJCZ1VWdlNHd1RtdnZYSVliMHpOTVFoV2h2Q0N1NmZpcldnaSUyQlhNNjBwMnclMkJ5dmtNQlZDZ1dmRm92SHNrRDJSdUZtV3dka2o5QUhXY1o4N0klMkJ3dVptVHdpUnclM0QlM0Q; RSCondition=[{"CookieIndex":"20220526135436","Cndt_No":0,"M_Id":"","Jobtype_Code":"1000100,1000101,1000102,1000096,1000097,1000104,1000094,1000109,1000110","Employ_Type":"3","Reg_Dt":"2022-05-26T13:54:36.4912113+09:00","IsKeep":true},{"CookieIndex":"20220526135150","Cndt_No":0,"M_Id":"","Employ_Type":"3","Reg_Dt":"2022-05-26T13:51:50.8033792+09:00","IsKeep":true},{"CookieIndex":"20220524181321","Cndt_No":0,"M_Id":"","Jobtype_Code":"1000101,1000102,1000096,1000098,1000104,1000105,1000094,1000109,1000097,1000100","Edu_Level":"5","Employ_Type":"3","Reg_Dt":"2022-05-24T18:13:21.808864+09:00","IsKeep":true},{"CookieIndex":"20220524181246","Cndt_No":0,"M_Id":"","Jobtype_Code":"1000101,1000102,1000096,1000098,1000104,1000105,1000094,1000109,1000100,1000097","Edu_Level":"5","Employ_Type":"3","Reg_Dt":"2022-05-24T18:12:46.2932003+09:00","IsKeep":true},{"CookieIndex":"20220524181213","Cndt_No":0,"M_Id":"","Jobtype_Code":"1000101,1000102,1000096,1000097,1000098,1000104,1000105,1000094,1000109,1000100","Edu_Level":"5","Employ_Type":"3","Reg_Dt":"2022-05-24T18:12:13.0879047+09:00","IsKeep":true}]',
        'Origin': 'https://www.jobkorea.co.kr',
        'Referer': 'https://www.jobkorea.co.kr/recruit/joblist?menucode=local&localorder=1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'page': str(i),
        'condition[jobtype]': '3',
        'condition[duty]': '1000100,1000101,1000102,1000096,1000097,1000104,1000094,1000109,1000110',
        'condition[menucode]': '',
        'direct': '0',
        'order': '20',
        'pagesize': '40',
        'tabindex': '0',
        'fulltime': '0',
        'confirm': '0',
    }

    response = requests.post('https://www.jobkorea.co.kr/Recruit/Home/_GI_List/', cookies=cookies, headers=headers, data=data)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title_num = len(soup.select('.titBx')) # 40

    for j in range(0, 40):
        try:
            box = soup.select('.titBx')[j] # 여기만 숫자 변경
            title = box.select('a')[0].text
            company = soup.select('td.tplCo > a')[j].text
            link = 'https://www.jobkorea.co.kr/'+box.select('a')[0]['href']
            tag = box.select('.dsc')[0].text
            tag = tag.split(', ')
            dday = soup.select('td.odd > span.date.dotum')[j].text
            if '상시채용' in dday or '오늘마감' in dday or '내일마감' in dday:
                dday = dday
            else:
                dday = dday.replace('~', '').split('(')[0]
                month, day = dday.split('/')
                dday = '2022. '+month+'. '+day
            titles.append(title)
            ddays.append(dday)
            links.append(link)
            companies.append(company)
            tags.append(tag)
        except:
            break

for i in range(len(titles)):
    li_tmp = li_tmp = {"title": titles[i], "dday": ddays[i], "link": links[i], "company": companies[i], "tag": tags[i]}
    intern.append(li_tmp)  


# In[52]:


df = pd.DataFrame(intern)
df = df.drop_duplicates(['title'], keep='first')
df = df.sort_values(by=['dday'])
df = df.reset_index(drop=True)


# In[53]:


titles = []
ddays = []
links = []
companies= []
tags = []
intern = []
new_tags = []
check_app = ['iOS', '앱', '게임', '소프트웨어', '응용', '어플리케이션', '아이폰', '안드로이드']
check_AI = ['AI', 'IoT', '러닝', '인공지능']
check_web = ['웹', '엔드', 'HTML', 'web']
check_data = ['데이터', 'DB','Data']
check_server = ['서버', '블록체인', '보안']
check_system = ['Unix', 'Linux', '임베디드','시스템']

for i in range(len(df)):
    ttag = []
    title = df.iloc[i][0]
    dday = df.iloc[i][1]
    link = df.iloc[i][2]
    company = df.iloc[i][3]
    tag= df.iloc[i][4]
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

for i in range(len(titles)):
    li_tmp = {"title": titles[i], "dday": ddays[i], "link": links[i], "company": companies[i], "tag": tags[i], "bigtag":new_tags[i]}
    intern.append(li_tmp)


# In[54]:


with open('../json 결과/인턴십.json', 'w', encoding='UTF-8') as file:
     file.write(json.dumps(intern, ensure_ascii=False, indent="\t"))

