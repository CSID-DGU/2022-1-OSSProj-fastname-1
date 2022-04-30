import requests
from bs4 import BeautifulSoup
import json
import os
import sys

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

# 데이터를 받을 리스트
title_t = []
company_t = []
addr_t = []
link_t = []

# 5페이지까지 크롤링
for i in range(1, 2):
    # IT 직무 크롤링
    # url = 'https://www.saramin.co.kr/zf_user/search/recruit?searchword=%EC%A0%95%EB%B3%B4%EB%B3%B4%EC%95%88&go=&flag=n&searchMode=1&searchType=search&search_done=y&search_optional_item=n&recruitPage=' + str(i) + '&recruitSort=relation&recruitPageCount=40&inner_com_type=&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&quick_apply=&except_read='
    url = 'https://www.saramin.co.kr/zf_user/search?searchword=IT&go=&flag=n&searchMode=1&searchType=search&search_done=y&search_optional_item=n'
    #  + str(i) + '&recruitSort=relation&recruitPageCount=40&inner_com_type=&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&quick_apply=&except_read='

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    request = Request(url, headers=headers)
    response = urlopen(request)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    # 제목
    title = soup.select('#recruit_info_list > div.content > div > div.area_job > h2 > a > span')
    for t in title:
        title_t.append(t.text)

    # 회사명
    # company = soup.select('#recruit_info_list > div.content > div > div.area_corp > strong > a > span')
    # for t in company:
    #     company_t.append(t.text)

    # 회사 위치
    # addr = soup.select('#recruit_info_list > div.content > div > div.area_job > div.job_condition > span:nth-child(1)')
    # for t in addr:
    #     addr_t.append(t.text)

    # 채용 공고 링크
    link = soup.select('#recruit_info_list > div.content > div > div.area_job > h2 > a')
    'https://www.saramin.co.kr' + link[0]['href']
    for l in link:
        link_t.append('https://www.saramin.co.kr' + l['href'])

# 데이터 저장
col = ['기업명', '제목', '주소', '링크']
# data = pd.DataFrame(list(zip(company_t, title_t, addr_t, link_t)), columns=col)
# data.to_csv('saramin.csv', index=False)
# print("크롤링 완료")





BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# print('뉴스기사 스크래핑 시작')

# req = requests.get('https://www.yna.co.kr/safe/news') ##예시
# req = requests.get('https://www.saramin.co.kr/zf_user/jobs/list/job-category?exp_cd=1&edu_min=8&edu_max=11&cat_mcls=2&loc_mcd=101000&company_type=scale001%2Cscale002%2Cscale003&panel_type=&search_optional_item=y&search_done=y&panel_count=y') ##사람인 주소입력
# req.encoding= None
# html = req.content
# soup = BeautifulSoup(html, 'html.parser')

##사람인 공고 title 가져오기
# datas = soup.select( 
#     '#rec_link_42913596 > span'
#     # 'div.contents > div.content01 > div > ul > li > article > div > h3' ##예시
#     )
        

# data = {}

# for tag in datas:
#     print(tag.text)


# for title in datas:   
#     name = title.find_all('a')[0].text
#     print("name = "+name)
#     url = 'http:'+title.find('a')['href']
#     data[name] = url

with open(os.path.join(BASE_DIR, 'saramin_title.json'), 'w+',encoding='utf-8') as json_file:
    json.dump(title_t, json_file, ensure_ascii = False, indent='\t')

with open(os.path.join(BASE_DIR, 'saramin_link.json'), 'w+',encoding='utf-8') as json_file:
    json.dump(link_t, json_file, ensure_ascii = False, indent='\t')

print("공고 제목> ")
print(title_t)
print("링크> ")
print(link_t)

print("사람인 스크래핑 끝")




