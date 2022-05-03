import requests
from bs4 import BeautifulSoup as BS
import json
import re

def Crawling(html):
    temp_dict = {}
    tr_list = html.select('div.board_list > ul > li')
    tr_list = tr_list[7:16]
#    print(len(tr_list))

    for tr in tr_list:
        no = tr.find('span',{'class':'num'}).text    # 고유값 공지만 없애버리고 싶음..
        title = tr.find('p',{'class':'tit'}).text   # 제목
        title = title.strip()
        date = tr.find('div',{'class':'info'}).text   # 날짜
        date = date.split('\n')
        date = date[1]
        temp_dict[str(no)] = {'title':title, 'date':date}
        
    return temp_dict


def toJson(dgu_dict):
    with open('dgu_list.json', 'w', encoding='utf-8') as file :
        json.dump(dgu_dict, file, ensure_ascii=False, indent='\t')


dgu_dict = {}

for page in [1,5]: # 1페이지부터 5페이지
    req = requests.get('https://www.dongguk.edu/article/HAKSANOTICE/list/?pageIndex={}&'.format(page))
 
    html = BS(req.text, 'html.parser')
    
    dgu_dict = dict(dgu_dict, **Crawling(html))

for item in dgu_dict:
    print(item, dgu_dict[item]['title'], dgu_dict[item]['date'])
    
toJson(dgu_dict)
