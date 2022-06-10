# 프로젝트 제목: 동국대생을 위한 정보전달 웹사이트 '융알이'

# 프로젝트 내용:
### 프로젝트 개요
![그림 1](https://user-images.githubusercontent.com/101690336/173097715-4a85d96a-c3ea-4734-a859-136ec1f681de.png)
융알이는 다음과 같이 작동합니다. 먼저 파이썬으로 작성된 크롤링 파일이 깃허브 액션스를 통해 자동으로 실행됩니다. 실행파일은 대상으로 하는 사이트의 지정된 정보를 모두 가져와 json 으로 저장 및 자동으로 덮어쓰기 하여 충돌이 일어나지 않도록 제작했습니다. 
저장된 json 파일은 EC2 내 Node.js 서버를 통해 배포됩니다. 사이트 내에서 유저가 분류를 선택하지 않은 경우 모든 데이터를 출력하며 분류가 선택되면 자바스크립트에서 해당 분류에 따라 json 데이터를 가공하고 출력해줍니다. 


# 기능
1. 크롤링
2. 크롤링 자동화
3. 웹페이지

# 실행환경
### 배포방법: AWS EC2를 통해 배포
### 웹서버: nodejs

# 설치 방법
 * 작업환경
   * 파이썬 3.9.2
   * Node.js 서버
   * EC2

* 파이썬 설치
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
# 팀원 정보(연락처, 역할)
## [고상현] (https://github.com/hyun7520) 
연락처: sanghyun123452@gmail.com  
역할: 크롤링 코드 작성, 데이터 정리 및 분류

## [권석현] (https://github.com/sukhyun205)
연락처: sukhyun205@gmail.com  
역할: 서버 구축, 메뉴, 체크박스 구현, ui 개선- 화면 크기 조절에 따른 동적 변화

## [김동근] (https://github.com/kimdonggeun111)
연락처: kdgk9620@gmail.com  
역할: 크롤링 자동화, 캘린더, 분류기능, UI개선- 마우스 오버 및 클릭 이벤트 추가

## 코드 예제
- 
## 실제 적용 사례
= json 파일하고 웹페이지 실행 화면
