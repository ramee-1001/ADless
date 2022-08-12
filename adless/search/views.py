from django.shortcuts import redirect, render
from .models import blogList, Keyword


# Create your views here.
def index(request):
    blog_list = blogList.objects.all()
    context = {'blog_list' : blog_list}
    return render(
        request,
        'search/index.html',
        context
    )

def createform(request):
    import sys
    import urllib.request
    import json
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


    #속도향상 1
    chrome_options = Options()
    chrome_options.headless = True
    #속도향상 2
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"


    if request.method == "POST":
        quote = request.POST['word']
        
 
    client_id = "tpaHiK8EMySuAfeTPSI9" # 발급받은 id 입력
    client_secret = "vgeqI6XKIc" # 발급받은 secret 입력 
    #quote = input("검색어를 입력해주세요.: ") #검색어 입력받기
    encText = urllib.parse.quote(quote)

    url = "https://openapi.naver.com/v1/search/blog?query=" + encText +"&display=3" # json 결과
    url = url.replace(" ", "")

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

    #제목 다듬기
    blog_titles = []
    for i in titles:
        a = i.replace("<\/b","")
        b = a.replace("<b>","")
        c = b.replace(">","")
        d = c.replace("\\","")
        f = d.replace("&quot;",'"')
        
        blog_titles.append(f)

    # 링크를 다듬기 (필요없는 부분 제거 및 수정)
    blog_links = []
    for i in links:
        a = i.replace('\\','')
        b = a.replace('?Redirect=Log&logNo=','/')
        blog_links.append(b)

    #본문 크롤링
    import time
    from selenium import webdriver
    from bs4 import BeautifulSoup
    from selenium.webdriver.common.by import By

    driver = webdriver.Chrome('C:/Users/rlaqh/Downloads/chromedriver.exe', options=chrome_options) #chromedriver.exe 가있는 파일 위치 복사하여 입력
    driver.implicitly_wait(3)

    #블로그 링크 하나씩 불러서 크롤링
    contents = []
    for i in blog_links:
        #블로그 링크 하나씩 불러오기
        driver.get(i)
        
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
        #print('본문: \n', a)



    data = []
    i=0
    for t in contents:

        obj = {
            'title' : blog_titles[i],
            'link' : blog_links[i],
            'text' : t
        }
        data.append(obj)
        i+=1



    for item in data:
            blogList(title = item['title'], blogurl = item['link'], text = item['text']).save()
    
    return redirect('/search')

