import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from crawler.place import Place

options = webdriver.ChromeOptions()
options.add_argument('headless')

class NaverMapCrawler:
    __base_url: str = "https://map.naver.com/v5/search"
    # ChromeDriverManager가 알아서 Chrome driver의 경로를 찾아줌
    __driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options)
    
    __changeframe_timelimit: int = 0.5

    def __init__(self, changeframe_timelimit: int = None) -> None:
        self.__driver.get(self.__base_url)
        if changeframe_timelimit:
            self.__changeframe_timelimit = changeframe_timelimit


    def reset(self):
        self.__driver.get(self.__base_url)

    
    def search(self, keyword: str):
        tag = "div.input_box > input.input_search"
        self.__search_tag(tag)

        search = self.__driver.find_element(By.CSS_SELECTOR, tag)
        search.send_keys(keyword)
        search.send_keys(Keys.ENTER)

        time.sleep(1)

        self.__driver.switch_to.default_content()  # frame 초기화
        self.__driver.switch_to.frame("searchIframe")  # frame 변경

        return self.get_places()

    def get_places(self):
        next_btns = self.__driver.find_elements(By.CSS_SELECTOR, '.zRM9F> a')
        places: list[Place] = []

        for index, next_btn in enumerate(next_btns):
            if index == 0 or index == 1: continue # <, 1 btn 무시

            items = self.__driver.find_elements(By.CSS_SELECTOR, 'li.VLTHu')

            for item in items:
                places.append(Place(self.__driver, item, self.__changeframe_timelimit))

            if not next_btn.is_enabled():
                break
                
            next_btn.click()
            time.sleep(self.__changeframe_timelimit)
        
        return places


    def scroll(self, action: str, num: int):
        body = self.__driver.find_element(By.CSS_SELECTOR, 'body')
        body.click()

        for i in range(num):
            if action == "up":
                body.send_keys(Keys.PAGE_UP)
            elif action == "down":
                body.send_keys(Keys.PAGE_DOWN)
    

    def __search_tag(self, code: str):
        timelimit = 10
        try:
            wait = WebDriverWait(self.__driver, timelimit).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, code)))
        except:
            print(code, '태그를 찾지 못하였습니다.')
            self.__driver.quit()
        return wait