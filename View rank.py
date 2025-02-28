import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

query = "python flask"
target_blog_link = "https://blog.naver.com/loyz/223391727109"
검색쿼리들 =["python flask", "파이썬썬 selenium"]
target_blog_links = ["https://blog.naver.com/loyz/223391727109", "https://blog.naver.com/lread90"]
for 검색쿼리, target_blog_link in zip(검색쿼리들, target_blog_links):
    search_link = f"https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query={query}"
    driver.get(search_link)
    time.sleep(2)

    link_selector = f'a[href^="{target_blog_link}"]'
    
    현재랭크 = -1
    # 예외처리 구문
    blog_found = False
    for _ in range(7): #최대 7번 하위 랭크 블로그 글을 불러옴
        try:
            element = driver.find_element(By.CSS_SELECTOR, link_selector)
            while True:
                new_element = element.find_element(By.XPATH, "./..")
                현재랭크 = new_element.get_attribute("data-cr-rank")
                if 현재랭크 != None:
                   # print("현재랭크 찾음 : ", 현재랭크)
                    blog_found = True
                    break
                # print("현재랭크 못찾음")
                element = new_element
            if blog_found:
                break
        except:
            print("타겟 블로그를 못 찾음 -> 스크롤 하겠습니다.")
            driver.execute_script("window.scrollBy(0,10000);")
            time.sleep(3) # 새로운 글 로딩하는데 기다리는 시간
    pirnt(f"{query} / {현재랭크} : 타겟 블로그의 랭크를 찾았습니다.") 
input()