import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

class __PlaceAttribute:
    address: str = ""
    contact_number: str = ""
    job_category: str = ""
    name: str = ""
    working_time: str = ""
    review_cnt: int = 0
    rate_score: int = 0


class Place(__PlaceAttribute):
    __changeframe_timelimit: int = 0.5

    def __init__(self, handle: Chrome, element: WebElement, changeframe_timelimit: int) -> None:
        self.__handle = handle
        self.__rawdata = element
        self.__changeframe_timelimit = changeframe_timelimit

        self.__open_slide()
        # 정보가 적혀있는 iframe으로 변경
        self.__change_iframe("entryIframe")
        self.__set_details()
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

    def __set_details(self):
        try:
            top_elem = self.__handle.find_element(By.ID, "app-root")
        except:
            top_elem = None

        if not top_elem:
            return
        
        self.address = self.__get_text_from_elem(top_elem, By.CLASS_NAME, "LDgIH")
        self.contact_number = self.__get_text_from_elem(top_elem, By.CLASS_NAME, "xlx7Q")
        self.job_category = self.__get_text_from_elem(top_elem, By.CLASS_NAME, "lnJFt")
        self.name = self.__get_text_from_elem(top_elem, By.CLASS_NAME, "GHAhO")
        self.review_cnt = self.__get_text_from_elem(top_elem, By.CLASS_NAME, "place_section_count", 0)

        try:
            workingtime_div = top_elem.find_element(By.CLASS_NAME, "U7pYf")
            if workingtime_div:
                self.working_time = self.__get_text_from_elem(workingtime_div, By.TAG_NAME, "time")
        except:
            pass

        try:
            rate_score_div = top_elem.find_element(By.CLASS_NAME, "PXMot LXIwF")
            if rate_score_div:
                self.rate_score = self.__get_text_from_elem(rate_score_div, By.TAG_NAME, "span", 0)
        except:
            pass

    def __get_text_from_elem(self, elem: WebElement, by: str, value: str, default_value = None):
        try:
            return elem.find_element(by, value).text
        except:
            if default_value:
                return default_value
            return ""