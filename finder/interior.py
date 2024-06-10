from finder.finder import PlaceFinder

class InteriorFinder(PlaceFinder):
    def __init__(self, loading_wait: int | None, changeframe_wait: int | None) -> None:
        super().__init__(loading_wait, changeframe_wait)
    
    @property
    def keyword_postfix(self):
        return "인테리어 리모델링"