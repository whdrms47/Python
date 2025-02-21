import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()
driver.get("https://nid.naver.com")
time.sleep(1)

# 2. browser information
# 2-1. title ~ 웹 사이트의 타이틀을 가지고옴 
title = driver.title
print(title, "이 타이틀이다")
# 2-2. urrent_url ~ 주소창을 그대로 가지고옴 
curl = driver.current_url
print(curl, "가 현재주소이다")

if "nid.naver.com" in curl:
    print("로그인 하는 로직 필요")
else:
    print("내가 생각한 로직 그대로 노출")
input()