import os
from datetime import datetime
from finder import PlaceFinderFactory, FinderType, FoundPlaces

OUTPUT_DIR = "outputs"

regions = [
    "광교",
    "경기도 수원시",
    "동탄",
]

finder = PlaceFinderFactory.create(FinderType.INTERIOR, 1, 0.5)

if not finder:
    print('Invalid finder type')
    exit()

places = FoundPlaces([])

for region in regions:
    founds = finder.find(region).data
    print(f"Found {len(founds)} places in {region}")
    places.extend(founds)

csv = places.to_csv()

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

date, time = datetime.today().__str__().split(" ")
time = time.replace(":", "-").split(".")[0]

filename = f"{date}_{time}.csv"

with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as file:
    file.write(csv)