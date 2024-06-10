from finder import PlaceFinderFactory, FinderType

finder = PlaceFinderFactory.create(FinderType.INTERIOR)

if not finder:
    print('Invalid finder type')
    exit()

places = finder.find('경기도 수원시')

for place in places:
    print(place.name)
    print(place.address)
    print(place.contact_number)
    print(place.job_category)
    print(place.working_time)
    print(place.review_cnt)
    print(place.rate_score)
    print()