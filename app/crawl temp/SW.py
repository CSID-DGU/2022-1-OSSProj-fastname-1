import requests
from bs4 import BeautifulSoup as BS
import json

def Crawling(html):
    temp_dict = {}
    tr_list = html.select('table > tbody > tr')
    
#    print(len(tr_list))


    for tr in tr_list:
        no = tr.find('td',{'class':'num'}).text           
        title = tr.find('a').text
        date = tr.find('td',{'class':'date'}).text
        temp_dict[str(no)] = {'title':title, 'date':date}
        
    return temp_dict


def toJson(sw_dict):
    with open('sw_list.json', 'w', encoding='utf-8') as file :
        json.dump(sw_dict, file, ensure_ascii=False, indent='\t')


sw_dict = {}

for page in range(1,5): # 1페이지부터 n페이지까지
    req = requests.get('https://sw.dongguk.edu/board/list.do?id=S181&cat=C4&keyword=&page={}&range=1'.format(page))
 
    html = BS(req.text, 'html.parser')
    
    sw_dict = dict(sw_dict, **Crawling(html))
    
#for item in sw_dict:
#    print(item, sw_dict[item]['title'], sw_dict[item]['date'])
    
toJson(sw_dict)
