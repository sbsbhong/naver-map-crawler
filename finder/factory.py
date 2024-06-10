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
    def create(finder_type: FinderType, loading_wait: int = None, changeframe_wait: int = None) -> Union[PlaceFinder, None]:
        if finder_type == FinderType.INTERIOR:
            return InteriorFinder(loading_wait, changeframe_wait)
        elif finder_type == FinderType.TEAM:
            return TeamFinder(loading_wait, changeframe_wait)
        else:
            return None