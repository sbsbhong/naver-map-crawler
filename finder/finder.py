from naver import NaverMapCrawler
from naver.place import NaverMapPlace
from abc import ABCMeta, abstractmethod
from typing import Union
from finder.found import FoundPlaces



class PlaceFinder(metaclass=ABCMeta):
    def __init__(self, loading_wait: Union[int, None], changeframe_wait: Union[int, None]) -> None:
        self.__loading_wait: Union[int, None] = loading_wait
        self.__changeframe_wait: Union[int, None] = changeframe_wait

    @property
    @abstractmethod
    def keyword_postfix(self):
        pass

    @property
    def timeout(self):
        return self.__changeframe_wait

    def __resolve_keyword(self, region: str):
        return " ".join([region, self.keyword_postfix])
    
    def __drop_duplication(self, places: list[NaverMapPlace]) -> list[NaverMapPlace]:
        keys = set()
        result = []

        for place in places:
            if place.key not in keys:
                keys.add(place.key)
                result.append(place)
        
        return result

    def find(self, region: str) -> FoundPlaces:
        crawler = NaverMapCrawler(self.__loading_wait, self.__changeframe_wait)
        places = crawler.search(self.__resolve_keyword(region))
        crawler.close()

        return FoundPlaces(self.__drop_duplication(places))