import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()
# 1. Navigation 관련 툴

# 1-1. get() 원하는 페이지로 이동하는 함수
driver.get("https://www.naver.com")
time.sleep(1)
driver.get("https://www.google.com")

# 1-2. back() - 뒤로가기
driver.back()
time.sleep(1)

# 1-3. forward() - 앞으로가기
driver.forward()
time.sleep(2)

# 1-4. refresh() - 새로고침
driver.refresh()
time.sleep(2)
print("동작 끝 수고욤")
input()


