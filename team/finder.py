from crawler import NaverMapCrawler

SEARCH_KEYWORD_POSTFIX = "주짓수"

class TeamFinder:
    @staticmethod
    def find_teams(region: str):
        crawler = NaverMapCrawler()

        keyword = " ".join([region, SEARCH_KEYWORD_POSTFIX])

        return crawler.search(keyword)