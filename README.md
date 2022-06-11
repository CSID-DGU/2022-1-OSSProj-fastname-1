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

# 기능
1. 크롤링
2. 크롤링 자동화
3. 체크박스 분류기능

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
$ sudo apte install python3
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

# 팀원 정보(연락처, 역할)
## [고상현] (https://github.com/hyun7520) 
연락처: sanghyun123452@gmail.com  
역할: 크롤링 코드 작성, 데이터 정리 및 분류

## [권석현] (https://github.com/sukhyun205)
연락처: sukhyun205@gmail.com  
역할: 웹서버 구축 및 작업내용 적용(로컬, 배포환경), 체크박스 구현, UI 개선- 화면 크기 조절에 따른 동적 변화

## [김동근] (https://github.com/kimdonggeun111)
연락처: kdgk9620@gmail.com  
역할: 크롤링 자동화, 캘린더, 분류기능, UI개선- 마우스 오버 및 클릭 이벤트 추가

## 코드 예제
- 
## 실제 적용 사례
= json 파일하고 웹페이지 실행 화면


