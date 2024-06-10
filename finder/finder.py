from naver import NaverMapCrawler
from abc import ABCMeta, abstractmethod
from typing import Union

class PlaceFinder(metaclass=ABCMeta):
    def __init__(self, timeout: Union[int, None]) -> None:
        self.__timeout: Union[int, None] = timeout

    @property
    @abstractmethod
    def keyword_postfix(self):
        pass

    @property
    def timeout(self):
        return self.__timeout

    def __resolve_keyword(self, region: str):
        return " ".join([region, self.keyword_postfix])

    def find(self, region: str):
        crawler = NaverMapCrawler(self.__timeout)

        return crawler.search(self.__resolve_keyword(region))