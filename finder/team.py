from finder.finder import PlaceFinder

class TeamFinder(PlaceFinder):
    def __init__(self, loading_wait: int | None, changeframe_wait: int | None) -> None:
        super().__init__(loading_wait, changeframe_wait)
    
    @property
    def keyword_postfix(self):
        return "주짓수"