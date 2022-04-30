import requests
from bs4 import BeautifulSoup
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print('뉴스기사 스크래핑 시작')

req = requests.get('https://www.yna.co.kr/safe/news') ##예시
# req = requests.get('https://www.saramin.co.kr/zf_user/jobs/list/job-category?exp_cd=1&edu_min=8&edu_max=11&cat_mcls=2&loc_mcd=101000&company_type=scale001%2Cscale002%2Cscale003&panel_type=&search_optional_item=y&search_done=y&panel_count=y') ##사람인 주소입력
req.encoding= None
html = req.content
soup = BeautifulSoup(html, 'html.parser')

datas = soup.select( 
    # '#rec_link_42913596 > span'
    'div.contents > div.content01 > div > ul > li > article > div > h3' ##예시
    )
        

data = {}

for tag in datas:
    print(tag.text)


for title in datas:   
    name = title.find_all('a')[0].text
    print("name = "+name)
    url = 'http:'+title.find('a')['href']
    data[name] = url

with open(os.path.join(BASE_DIR, 'example.json'), 'w+',encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii = False, indent='\t')

print(data)
print(datas)

print("뉴스기사 스크래핑 끝")





