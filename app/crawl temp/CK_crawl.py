#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
from bs4 import BeautifulSoup
import selenium
import time
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException


# In[2]:


#frm > div > div.list_style_2 > ul > li.imminent > div.title > a
#frm > div > div.pagination > ul > li:nth-child(1)
#frm > div > div.pagination
#frm > div > div.list_style_2 > ul > li:nth-child(4) > ul > li.icon_2
#frm > div > div.list_style_2 > ul > li.imminent > div.title > a > span.txt


# In[3]:


result = {
    "title": [],
    "date" : [],
    "category": [],
    "link": []
}
target = ['대학생', '일반인', '누구나']

driver = webdriver.Chrome(executable_path='chromedriver')
driver.get('https://www.contestkorea.com/sub/list.php?int_gbn=1&Txt_bcode=030210001') #크롬 페이지를 하나 여러 확인하는 용도, 코드 완료 시 삭제 해야함

driver.find_element_by_css_selector('#frm > div > div.clfx.mb_20 > div.f-r > ul > li:nth-child(4) > button').click()
time.sleep(1)

for n in range(1, 5):
    
    response = requests.get(driver.current_url)

    if response.status_code == 200:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        list_crawl = soup.select('#frm > div > div.list_style_2 > ul')
    else : 
        print(response.status_code)

    for li in list_crawl:        
        for num in range(0, 11):
            tmp = []
            
            try:
                li_target = li.select('li > ul > li.icon_2')[num].get_text()
                if any(word in li_target for word in target):
                    li_title = li.select('li > div.title > a > span.txt')[num].get_text()
                    li_date_tmp = li.select('li > div.date > div > span.step-1')[num].text
                    li_date = li_date_tmp.replace("\n", "").replace("\t", "")
                    link_tmp = li.select('li > div.title > a')[num]
                    link = link_tmp['href']               
                    result["title"].append(li_title)
                    result["date"].append(li_date)
                    result["link"].append("https://www.contestkorea.com/sub/" + link)
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
            result["category"].append(tmp)
                
    '''
    page_next = driver.find_element_by_css_selector('#frm > div > div.pagination > ul > *')
    page_sign = driver.find_element_by_css_selector('#frm > div > div.pagination > button.mg_right')
    '''
    
    try:
        if n%5 != 0:
            text = str(n%5 + 1)
            driver.find_element_by_link_text(text).click()
    except NoSuchElementException:
        driver.close()
        break

    time.sleep(1)


# In[4]:


for key, value in result.items():
    print(key, value)


# In[5]:


import json

print(json.dumps(result, ensure_ascii=False, indent="\t"))
# JSON 생성 시 형태 확인


# In[6]:


with open('result.json', 'w', encoding="utf-8") as make_file: 
    json.dump(result, make_file, ensure_ascii = False, indent="\t")


# In[7]:


import pandas as pd
df = pd.DataFrame(result)
df


# In[ ]:




