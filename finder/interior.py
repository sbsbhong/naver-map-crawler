from finder.finder import PlaceFinder

class InteriorFinder(PlaceFinder):
    def __init__(self, timeout: int | None) -> None:
        super().__init__(timeout)
    
    @property
    def keyword_postfix(self):
        return "인테리어 리모델링"