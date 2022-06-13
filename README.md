# 프로젝트 제목: 동국대생을 위한 정보전달 웹사이트 '융알이'



# 프로젝트 내용:
### 프로젝트 개요
<p align='center'>
<img src="https://user-images.githubusercontent.com/101690336/173097715-4a85d96a-c3ea-4734-a859-136ec1f681de.png">
</p>

* 융알이는 다음과 같이 작동합니다. 먼저 파이썬으로 작성된 크롤링 파일이 깃허브 액션스를 통해 자동으로 실행됩니다. 실행파일은 대상으로 하는 사이트의 지정된 정보를 모두 가져와 json 으로 저장 및 자동으로 덮어쓰기 하여 충돌이 일어나지 않도록 제작했습니다. 
* 저장된 json 파일은 EC2 내 Node.js 서버를 통해 배포됩니다. 사이트 내에서 유저가 분류를 선택하지 않은 경우 모든 데이터를 출력하며 분류가 선택되면 자바스크립트에서 해당 분류에 따라 json 데이터를 가공하고 출력해줍니다. 

# 메인페이지
![배포](https://user-images.githubusercontent.com/91311610/173172914-1c8d3719-4373-4989-81b5-e7e6369d541c.png)


# 실행 및 배포환경
<p align='center'>
<img src="https://user-images.githubusercontent.com/91311610/173174063-dceb803e-2ee7-4178-98a6-5d5c13413948.png" width="500" height="200">
</p>


#### 웹서버: Node.js Express 
#### 배포: AWS EC2 인스턴스
- AWS EC2 인스턴스 내 Node.js Express 웹서버를 통해 실행 및 배포
- 웹 브라우저에서 "EC2 Public IP address: port number"를 통해 접속





# 설치 방법
 * 작업환경
   * 파이썬 3.9.2
   * AWS EC2 인스턴스
   * Node.js 16.15.0


### 파이썬 설치
```c
$ sudo apt-get update
$ sudo apt install python3
$ sudo apt install python3-pip
```
* 파이썬 버전 확인
```c
$ python --version
$ pip -- version
```
* Beautifulsoup4 설치
```c
$ sudo apt-get update
$ pip install beautifulsoup4 
```
* pandas 설치
```c
$ sudo apt-get update
$ pip install pandas 
```
* requests 설치
```c
$ sudo apt-get update
$ pip install requests
```

### AWS EC2 인스턴스 연결

#### 1) 인스턴스 시작
![시작](https://user-images.githubusercontent.com/91311610/173173438-037b8129-ad2a-4f31-9db0-44507facd858.png)
#### 2) 프로토콜 및 포트범위 설정
![포트넘버](https://user-images.githubusercontent.com/91311610/173173369-086e666d-0192-4a70-a7b0-de0a761f5844.png)
#### 3) 인스턴스 연결
<img src="https://user-images.githubusercontent.com/91311610/173173546-28859cf2-90e0-4770-aff4-332ff62b1b84.png" width="592" height="350">


### Node.js 설치
```c
$ sudo apt-get install nodejs
```
* NPM(Node Package Manager) 설치
```c
$ sudo apt-get install npm
```
* Express 설치 및 package.json 정리
```c
$ npm install express --save
```
* 서버 동작을 위한 app.js 실행
```c
$ node app.js
```

## 코드 예제
- 크롤링 예시 (사람인 인턴십 정보)
```c
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
            if '채용시' in dday or '마감' in dday or '상시' in dday:
                dday = dday.split('(')[0]
            else:
                dday = dday.replace('~', '').split(' ')[0]
                month, day = dday.split('.')
                month = int(month)
                day = int(day)
                if month < today_month:
                    dday = '2023. '+ str(month) +'. '+str(day)
                else:
                    dday = '2022. '+ str(month)+'. '+str(day)

        except:
            break
        titles.append(title)
        ddays.append(dday)
        links.append(link)
        companies.append(company)
        tags.append(tag)
```
- AJAX 기반 사이트 크롤링 예시 (curl 변환기 사용)
```c
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
```
- json 저장 예시 (인턴 정보)
```c
for i in range(len(titles)):
    li_tmp = li_tmp = {"title": titles[i], "dday": ddays[i], "link": links[i], "company": companies[i], "tag": tags[i]}
    intern.append(li_tmp)

with open('../json 결과/인턴십.json', 'w', encoding='UTF-8') as file:
     file.write(json.dumps(intern, ensure_ascii=False, indent="\t"))
```

- 크롤링 자동화
```c
- name: Run Crawler
      run: |
        python "공모전, 대외활동 - 인크루트, 씽콘, 콘테스트_코리아, 씽유, 스펙토리.py"
        python "스터디, 프로젝트 모집 - okky, 인프런.py"
        python "인턴십 - 사람인, 잡코리아, 인크루트.py"
        python "장학금, 지원금 - 드림스폰.py"
        python "취업 - 잡코리아, 프로그래머스.py"
      working-directory: ${{ env.working-directory }}

    - name: commits
      run: |
        git config --global user.email "kdgk9620@gmail.com"
        git config --global user.name "kimdonggeun111"
        git add -A
        git commit -m "update Crawling files"
      working-directory: ${{ env.working-directory }}

    - name: Push
      uses: ad-m/github-push-action@master
      with:
        branch: 'main'
        github_token: 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
```

- 선택 버튼 이벤트
```c
function gettag(){ 
    check = ""; // 체크 초기화
    var storage = document.getElementsByName("tag"); // 태그 값이라는 이름을 가진 구성요소에 접근해서 태그가 붙어있는 문서의 내용만 storage에 저장
    for (i =0;i < storage.length;i++){ // storage수만큼 루프
       if((storage[i].bigtag).includes(checkList[j])){ // 만약 체크되어 있으면
         check += storage[i].value; // 아이프레임에 전달할 변수의 값(check)을 체크박스의 값으로 문자열에 추가
         check += "," // 구분자 추가
         //check = storage[i].value; // 아이프레임에 전달할 변수의 값(check)
       }
     }
     document.getElementById("if1").src += ''; // 웹페이지 갱신
     document.getElementById("if2").src += '';
     document.getElementById("if3").src += '';
     document.getElementById("if4").src += '';
     document.getElementById("if5").src += '';
}
```

- 체크박스 1개 이상 체크시 출력
```c
for(i in storage) { 
  selectx[i] = false; // 방문 배열을 초기화
  let tr = document.createElement('tr'); 
  for(j=0;j<(lenCheckList-1);j++){ // 마지막은 공백이라 길이에서 1을 뺌
      if((storage[i].bigtag).includes(checkList[j])){// 태그에 충족되면 출력
          if(selectx[i] == false){ // 이전에 선택되지 않았다면
              let td = document.createElement('td'); 
              td.innerHTML = storage[i].title; 
              td.setAttribute("title", storage[i].bigtag); // 마우스 오버 시 분류 출력
              Link = storage[i].link; 
              (function(m){  // 제목 클릭 시 링크로 이동(클로저 사용)
                  td.addEventListener("click", function() {location.href = storage[m].link;});
              })(i);
              tr.appendChild(td); 
              let td2 = document.createElement('td');
              td2.innerHTML = storage[i].dday; 
              tr.appendChild(td2);
              selectx[i] = true; // 방문배열을 방문함으로 변경 
          }    
      }
  document.querySelector("tbody").appendChild(tr);   
  }      
}
```
## 실제 적용 사례
[웹페이지 시연 영상](https://drive.google.com/file/d/1eB0O31y0sKb1N7OpAEPFrC5HR1VcgTAm/view?usp=sharing)

# 팀원 정보(연락처, 역할)
## [고상현](https://github.com/hyun7520) 
연락처: sanghyun123452@gmail.com  
역할: 크롤링 코드 작성, 데이터 정리 및 분류

## [권석현](https://github.com/sukhyun205)
연락처: sukhyun205@gmail.com  
역할: 웹서버 구축 및 작업내용 적용(로컬, 배포환경), 체크박스 구현, UI 개선- 화면 크기 조절에 따른 동적 변화

## [김동근](https://github.com/kimdonggeun111)
연락처: kdgk9620@gmail.com  
역할: 크롤링 자동화, 캘린더, 분류기능, UI개선- 마우스 오버 및 클릭 이벤트 추가

## 사용한 오픈소스
- [템플릿 오픈소스](https://codepen.io/AndreCortellini/pen/xxqbmg)
- [깃허브 푸시 자동화 오픈소스](https://github.com/marketplace/actions/add-commit)
- [CURL 변환 오픈소스](https://github.com/curlconverter/curlconverter)

## 라이선스
- MIT
