import time
import hashlib
from datetime import datetime
from typing import Union
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

class _Link:
    def __init__(self, elem: WebElement) -> None:
        self.href = elem.get_attribute("href")
        self.text = elem.text

    def __str__(self) -> str:
        return f"{self.text}: {self.href}"

class _PlaceAttributes:
    key: str
    address: Union[str, None]
    contact_number: Union[str, None]
    job_category: Union[str, None]
    name: Union[str, None]
    visitor_reviews: int
    blog_reviews: int
    gen_link: Union[_Link, None]
    link1: Union[_Link, None]
    link2: Union[_Link, None]
    link3: Union[_Link, None]

class NaverMapPlace(_PlaceAttributes):
    __changeframe_timelimit: int

    def __init__(self, handle: Chrome, element: WebElement, changeframe_timelimit: int) -> None:
        self.__handle = handle
        self.__rawdata = element
        self.__changeframe_timelimit = changeframe_timelimit

        self.__open_slide()
        # 정보가 적혀있는 iframe으로 변경
        self.__change_iframe("entryIframe")
        self.__set_props()
        # 부모 iframe로 변경
        self.__change_iframe("searchIframe")

    @property
    def rawdata(self):
        return self.__rawdata
    
    def __open_slide(self):
        self.rawdata.find_element(By.CLASS_NAME, "P7gyV").click()
        time.sleep(self.__changeframe_timelimit)

    def __change_iframe(self, name: str):
        self.__handle.switch_to.default_content()
        self.__handle.switch_to.frame(name)
        time.sleep(self.__changeframe_timelimit)

    def __set_props(self):
        try:
            top_elem = self.__handle.find_element(By.ID, "app-root")
        except:
            top_elem = None

        if not top_elem:
            return
        
        self.address = self.__get_element(top_elem, By.CLASS_NAME, "LDgIH")
        self.contact_number = self.__get_element(top_elem, By.CLASS_NAME, "xlx7Q")
        self.job_category = self.__get_element(top_elem, By.CLASS_NAME, "lnJFt")
        self.name = self.__get_element(top_elem, By.CLASS_NAME, "GHAhO")

        self.gen_link = self.__get_link(top_elem, By.CSS_SELECTOR, "div.jO09N > a")
        self.link1 = self.__get_link(top_elem, By.CSS_SELECTOR, 'div.Cycl8 > span:nth-of-type(1) > a')
        self.link2 = self.__get_link(top_elem, By.CSS_SELECTOR, 'div.Cycl8 > span:nth-of-type(2) > a')
        self.link3 = self.__get_link(top_elem, By.CSS_SELECTOR, 'div.Cycl8 > span:nth-of-type(3) > a')

        visitor_reviews = self.__get_element(top_elem, By.CSS_SELECTOR, "div.dAsGb > span:nth-of-type(1) > a")
        if visitor_reviews:
            self.visitor_reviews = int(visitor_reviews.split(" ")[1].replace(",", ""))
        else:
            self.visitor_reviews = 0

        blog_reviews = self.__get_element(top_elem, By.CSS_SELECTOR, "div.dAsGb > span:nth-of-type(2) > a")
        if blog_reviews:
            self.blog_reviews = int(blog_reviews.split(" ")[1].replace(",", ""))
        else:
            self.blog_reviews = 0

        name = self.name if self.name else datetime.today().__str__()
        address = self.address if self.address else ""
        key = "!@#$%".join([name, address])
        key = key.encode()
        hash = hashlib.sha256()
        hash.update(key)

        self.key = hash.hexdigest()

    def __get_element(self, elem: WebElement, by: str, identifier: str, child: str = None) -> Union[str, None]:
        try:
            found = elem.find_element(by, identifier)
            if child:
                found = found.find_element(By.TAG_NAME, child)
            return found.text
        except:
            return None
        
    def __get_link(self, elem: WebElement, by: str, identifier: str) -> Union[_Link, None]:
        try:
            found = elem.find_element(by, identifier)
            return _Link(found)
        except:
            return None
        
    def __str__(self) -> str:
        base = f"""{self.name} / {self.job_category}
- 주소: {self.address}
- 전화번호: {self.contact_number}
- 방문자 리뷰: {self.visitor_reviews} / 블로그 리뷰: {self.blog_reviews}"""
        
        if self.gen_link:
            base += f"""
- 대표 링크: {self.gen_link}
"""
        if self.link1:
            base += f"""
    . {self.link1}
"""
            
        if self.link2:
            base += f"""
    . {self.link2}
"""
            
        if self.link3:
            base += f"""
    . {self.link3}
"""
        return base