import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from naver.place import NaverMapPlace

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('start-maximized')
options.add_argument('window-size=1920,1080')


class NaverMapCrawler:
    __base_url: str = "https://map.naver.com/v5/search"
    # ChromeDriverManager가 알아서 Chrome driver의 경로를 찾아줌
    __driver: webdriver.Chrome 
    
    __loading_wait: int = 2
    __changeframe_wait: int = 0.5

    def __init__(self, loading_delay:int = None, changeframe_wait: int = None) -> None:
        self.__driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options)

        self.__driver.get(self.__base_url)

        if loading_delay:
            self.__loading_wait = loading_delay
        if changeframe_wait:
            self.__changeframe_wait = changeframe_wait

    def close(self):
        self.__driver.close()
    
    def quit(self):
        self.__driver.quit()
    
    def search(self, keyword: str):
        tag = "div.input_box > input.input_search"
        self.__search_tag(tag)

        search = self.__driver.find_element(By.CSS_SELECTOR, tag)
        search.send_keys(keyword)
        search.send_keys(Keys.ENTER)

        time.sleep(self.__loading_wait)

        self.__driver.switch_to.default_content()  # frame 초기화
        self.__driver.switch_to.frame("searchIframe")  # frame 변경

        return self.get_places()

    def get_places(self):
        next_btns = self.__driver.find_elements(By.CSS_SELECTOR, '.zRM9F> a')
        places: list[NaverMapPlace] = []

        time.sleep(self.__loading_wait)

        for i, next_btn in enumerate(next_btns):
            if i == 0 or i == 1: continue # <, 1 btn 무시
            
            # Lazy loading이 적용된 list로, 스크롤을 전부 내려야만 렌더링됨
            self.scroll("down", 30)
            time.sleep(self.__changeframe_wait)
            self.scroll("down", 30)
            time.sleep(self.__changeframe_wait)

            items = self.__driver.find_elements(By.CSS_SELECTOR, "div.Ryr1F > ul > li")

            try:
                for item in items:
                    places.append(NaverMapPlace(self.__driver, item, self.__changeframe_wait))
            except Exception as e:
                self.quit()
                raise e

            if not next_btn.is_enabled():
                break
                
            next_btn.click()
            time.sleep(self.__changeframe_wait)

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