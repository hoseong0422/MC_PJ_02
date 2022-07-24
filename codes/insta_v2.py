from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import pandas as pd

import urllib 
import platform


"""
망고테이블에서 수집된 식당 이름을 이용하여 인스타그램에 검색
DB에 저장하며 JOIN하여 조회할때 기준을 식당 이름으로 정했기 때문에
망고테이블에서 수집된 이름을 그대로 사용
"""
df_result = pd.read_csv("data/seoul_result.csv")
df_result["name"] = df_result["name"].str.replace(" ", "")
len(df_result["name"].values)

# 맥이면 이렇게
if platform.system() == 'Darwin':
    def get_chrome_driver():
        # 1. 크롬 옵션 세팅
    #chrome_options = webdriver.ChromeOptions()
    
    # 2. driver 생성하기
        driver = webdriver.Chrome(
            executable_path="/opt/homebrew/bin/chromedriver"
            )
    
        return driver

# 윈도우면 이렇게
elif platform.system() == 'Windows':
    def get_chrome_driver():
        # 1. 크롬 옵션 세팅
        chrome_options = webdriver.ChromeOptions()

        # 2. driver 생성하기
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), # 가장 많이 바뀐 부분
           options=chrome_options
        )
    
        return driver
else:
    print('Unknown System... sorry~~~~')


## 좋아요 가져오기
"""
좋아요 숨김 처리시 해당 element를 찾을수가 없기때문에
NoSuchElementException 에러가 발생하는데
예외처리를 사용하여 숨김처리 된 post들은 
여러 명이 좋아합니다.로 저장되도록 하였음
"""
def get_like():
    try:       
        like = driver.find_element(By.CSS_SELECTOR, "section._aam_ > div > div > div > a > div > span").text
        likes.append(like)
    except:
        like = "여러 명이 좋아합니다."
        likes.append(like)

# 포스트 내용 가져오기
def get_post():
    try:
        post = driver.find_element(By.CSS_SELECTOR,"span._aacl").text.replace("\n", " ")
        posts.append(post)
    
    # 중간에 화면 로딩 오류나면 다음 버튼 한번 눌러주기
    except:
        driver.find_element(By.CSS_SELECTOR,"div._aank > div > button").click()
        time.sleep(3)

# 태그 가져오기
def get_tag():
    
    tags_element = driver.find_elements(By.CSS_SELECTOR,"span._aacl > a")
    
    tmp_list = []
    for elm in tags_element:
        tag = elm.text
        tmp_list.append(tag)
    
    tags.append(tmp_list)

# 검색 전 준비하기
def ready_for_search():
    
    ID = "ID"
    PWD = "PWD"
    
    # ID 입력
    driver.find_element(By.CSS_SELECTOR,"input._2hvTZ").click()
    driver.find_element(By.CSS_SELECTOR,"input._2hvTZ").send_keys(f"{ID}")
    
    # Password 입력
    driver.find_element(By.CSS_SELECTOR,"#loginForm > div > div:nth-child(2) > div > label > input").click()
    driver.find_element(By.CSS_SELECTOR,"#loginForm > div > div:nth-child(2) > div > label > input").send_keys(f"{PWD}")
    
    time.sleep(1)
    
    # 로그인 버튼 클릭
    driver.find_element(By.CSS_SELECTOR,"#loginForm > div > div:nth-child(3) > button").click()
    
    time.sleep(5)
    
    # 정보 나중에 저장 클릭
    driver.find_element(By.CSS_SELECTOR, "#react-root > section > main > div > div > div > section > div > button").click()
    
    time.sleep(5)
    
    # 알림 설정 나중에하기
    driver.find_element(By.CSS_SELECTOR,"button._a9--._a9_1").click()

# 게시글 돌며 스크래핑
def scrap(n):
    for i in range(1, n):
        
        # 두번째 포스트 이후 다음 게시물 버튼
        if i > 2:
            driver.find_element(By.CSS_SELECTOR, "div._aaqg > button").click()
        
            time.sleep(3)
        
            get_like() # 좋아요 가져오기
            get_post() # 포스트 내용 가져오기
            get_tag() # 태그만 가져오기
        
            i += 1
        
        # 첫번째 포스트 클릭
        elif i == 1:
            driver.find_element(By.CSS_SELECTOR,"div._aagu > div._aagw").click()
            
            time.sleep(3)
        
            get_like() # 좋아요 가져오기
            get_post() # 포스트 내용 가져오기
            get_tag() # 태그만 가져오기
            
            i += 1
        
        # 첫번째 포스트에서 다음 게시물 버튼
        elif i == 2:

            driver.find_element(By.CSS_SELECTOR,"div._aank > div > button").click()
            
            time.sleep(3)
            
            get_like() # 좋아요 가져오기
            get_post() # 포스트 내용 가져오기
            get_tag() # 태그만 가져오기
            
            i += 1

keyword_list = df_result["name"].values

driver = get_chrome_driver()
driver.get("https://www.instagram.com/")
# 최초 로그인하고 검색을 완료하기 까지 로딩시간이 오래 걸려 15초 sleep 조건 설정
time.sleep(15)

# 실행하기
ready_for_search()
time.sleep(15)

posts_count = []

for keyword in keyword_list[:30]:
    
    likes = []
    posts = []
    tags = []
    # 검색어 입력이 아닌 URL로 검색어 직접 요청으로 변경
    parsed_keyword=urllib.parse.quote(keyword)
    try:
        driver.get(f"https://www.instagram.com/explore/tags/{parsed_keyword}")
        time.sleep(15)
    
        cnt = driver.find_element(By.CSS_SELECTOR,"span._ac2a").text.replace(",","")
        posts_count.append(cnt)
        time.sleep(2)
    except:
        continue
    
    # 가게별로 몇개의 포스트를 모아올건지?
    try:
        scrap(1)
    except:
        continue
    
    # 다음 검색어 입력 전 현재 선택된 포스트화면을 끄기위해 esc입력
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    df1 = pd.DataFrame(list(zip(posts, tags, likes)), columns=['content', 'tags', 'likes'])
    df1.to_csv(f"data/{keyword}.csv")

    # 저장이 완료된 dataframe삭제
    del df1
    
    # 저장이 완료된 리스트 삭제
    likes.clear()
    posts.clear()
    tags.clear()

df2 = pd.DataFrame(list(zip(keyword_list, posts_count)), columns = ["name", "post_cnt"])
df2.to_csv(f"data/Seoul_restoraunts_info.csv")
del df2
    
driver.close()