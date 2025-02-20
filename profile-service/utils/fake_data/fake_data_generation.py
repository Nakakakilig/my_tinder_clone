import random

from faker import Faker

fake = Faker("uk_UA")

TOP_RIGHT_LATITUDE = 52.16
TOP_RIGHT_LONGITUDE = 22.00

BOTTOM_LEFT_LATITUDE = 44.80
BOTTOM_LEFT_LONGITUDE = 40.12


def calc_loc(loc1, loc2):
    return random.randint(int(loc1 * 100), int(loc2 * 100)) / 100


run = True
locations = []
for i in range(10):
    lat = calc_loc(BOTTOM_LEFT_LATITUDE, TOP_RIGHT_LATITUDE)
    lot = calc_loc(TOP_RIGHT_LONGITUDE, BOTTOM_LEFT_LONGITUDE)
    print(f"{lat}, {lot}, {fake.name()}, {random.randint(18, 50)}")
