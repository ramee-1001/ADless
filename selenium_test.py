#코드 실행 전에 pip install selenium, pip install bs4, 
# 버전에 맞는 chromedriver 설치 해야함

import os
import sys
import urllib.request
import json
from selenium.common.exceptions import NoSuchElementException

client_id = "tpaHiK8EMySuAfeTPSI9" # 발급받은 id 입력
client_secret = "vgeqI6XKIc" # 발급받은 secret 입력 
quote = input("검색어를 입력해주세요.: ") #검색어 입력받기
encText = urllib.parse.quote(quote)
display_num = input("검색 출력결과 갯수를 적어주세요.(최대100, 숫자만 입력): ") #출력할 갯수 입력받기
url = "https://openapi.naver.com/v1/search/blog?query=" + encText +"&display="+display_num# json 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    #print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

body = response_body.decode('utf-8')
print('body \n', body)

#불필요한 큰따옴표 지우기
body = body.replace('"','')

#body를 나누기
list1 = body.split('\n\t\t{\n\t\t\t')
#naver블로그 글만 가져오기
list1 = [i for i in list1 if 'naver' in i]
print("list1 \n",list1)

#블로그 제목, 링크 뽑기
import re
titles = []
links = []
for i in list1:
    title = re.findall('title:(.*?),\n\t\t\tlink',i)
    link = re.findall('link:(.*?),\n\t\t\tdescription',i)
    titles.append(title)
    links.append(link)
 
titles = [r for i in titles for r in i]
links = [r for i in links for r in i]

print('<<제목 모음>>')
print(titles)
print('총 제목 수: ',len(titles),'개')#제목갯수확인
print('\n<<링크 모음>>')
print(links)
print('총 링크 수: ',len(links),'개')#링크갯수확인

# 링크를 다듬기 (필요없는 부분 제거 및 수정)
blog_links = []
for i in links:
    a = i.replace('\\','')
    b = a.replace('?Redirect=Log&logNo=','/')
    blog_links.append(b)

print(blog_links)
print('생성된 링크 갯수:',len(blog_links),'개')

#본문 크롤링
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('C:/Users/rlaqh/Downloads/chromedriver.exe') #chromedriver.exe 가있는 파일 위치 복사하여 입력
driver.implicitly_wait(3)

#블로그 링크 하나씩 불러서 크롤링
contents = []
for i in blog_links:
    #블로그 링크 하나씩 불러오기
    driver.get(i)
    time.sleep(1)
    #블로그 안 본문이 있는 iframe에 접근하기
    driver.switch_to.frame("mainFrame")
    #본문 내용 크롤링하기
    try:
        a = driver.find_element(By.CSS_SELECTOR, 'div.se-main-container').text
        contents.append(a)
    # NoSuchElement 오류시 예외처리(구버전 블로그에 적용)
    except NoSuchElementException:
        a = driver.find_element(By.CSS_SELECTOR, 'div#content-area').text
        contents.append(a)
    #print(본문: \n', a)




driver.quit() #창닫기
print("<<본문 크롤링이 완료되었습니다.>>")

#제목 및 본문 txt에 저장
total_contents = titles + contents

text = open("C:/tesseract/blog_crawling/blog_text.txt",'w',encoding='utf-8') #저장 경로 설정
for i in total_contents:
    text.write(i)
text.close()

#Dataframe으로 만들기
import pandas as pd

blog_data = pd.DataFrame({'제목':titles, '링크':blog_links,'내용':contents})
blog_data.to_csv('C:/tesseract/blog_crawling/blog_data.csv',index = False, encoding="utf-8-sig")
