from abc import ABCMeta
from typing import Union
from naver.place import NaverMapPlace

class FoundPlaces(metaclass=ABCMeta):
    __HEADERS = [
        "아이디", "이름", "직종", "전화번호",
        "주소(도로명)", "방문자 리뷰 수", "블로그 리뷰 수", 
        "대표 링크"
    ]

    def __init__(self, data: list[NaverMapPlace]) -> None:
        self.__count = 0
        self.__data = data

    @property
    def data(self) -> list[NaverMapPlace]:
        return self.__data
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.__count < self.__len__():
            self.__count += 1
            return self[self.__count - 1]
        else:
            self.__count = 0
            raise StopIteration

    def __getitem__(self, index):
        if index < self.__len__():
            return self.data[index]
        else:
            raise IndexError
    
    def __len__(self):
        return self.data.__len__()
    
    def extend(self, other: list[NaverMapPlace]):
        self.__data.extend(other)
    
    def to_csv(self, instead_comma: str = "-") -> list[list[str]]:
        table = self.to_table()
        duplicated = set()
        _csv = []

        headers = table[0]

        for row in table:
            _row = []

            if row[0] in duplicated:
                continue
            else:
                duplicated.add(row[0])

            for item in row:
                if isinstance(item, int):
                    item = str(item)
                elif item is None:
                    item = ""
                elif item.find(","):
                    item = item.replace(",", instead_comma)

                _row.append(item)
            
            if _row.__len__() < headers.__len__():
                for i in range(headers.__len__() - _row.__len__()):
                    _row.append("")
                
            _csv.append(",".join(_row))
        
        return "\n".join(_csv)
    
    def to_table(self) -> list[list[Union[str, int, None]]]:
        headers = self.__HEADERS
        rows = []

        for place in self.data:
            row = [
                place.key, place.name, place.job_category, place.contact_number, 
                place.address, place.visitor_reviews, place.blog_reviews
            ]

            if place.gen_link: row.append(place.gen_link.href)
            else: row.append("")

            for link in [place.link1, place.link2, place.link3]:
                if not link:
                    continue
                
                header_index = 0

                try:
                    header_index = headers.index(link.text)
                except ValueError:
                    # 헤더를 찾지 못한 경우 추가. (ex. 인스타그램이 없다면 인스타그램 추가)
                    headers.append(link.text)
                    header_index = headers.__len__() - 1

                if headers.__len__() != row.__len__():
                    # 길이의 차이 만큼 빈 문자열 삽입
                    for __ in range(headers.__len__() - row.__len__()):
                        row.append("")
                
                row[header_index] = link.href
            rows.append(row)
        
        rows.insert(0, headers)
        return rows
