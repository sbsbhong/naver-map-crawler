from finder.finder import PlaceFinder

class TeamFinder(PlaceFinder):
    def __init__(self, timeout: int | None) -> None:
        super().__init__(timeout)
    
    @property
    def keyword_postfix(self):
        return "주짓수"