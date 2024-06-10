from enum import Enum
from typing import Union
from finder.finder import PlaceFinder
from finder.team import TeamFinder
from finder.interior import InteriorFinder

class FinderType(Enum):
    INTERIOR = 'interior'
    TEAM = 'team'

class PlaceFinderFactory:
    @staticmethod
    def create(finder_type: FinderType, timeout: int = None) -> Union[PlaceFinder, None]:
        print(finder_type)
        if finder_type == FinderType.INTERIOR:
            return InteriorFinder(timeout)
        elif finder_type == FinderType.TEAM:
            return TeamFinder(timeout)
        else:
            return None