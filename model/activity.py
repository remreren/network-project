from json import JSONDecoder
from typing import List

class Activity(object):
    activity_name: str

    def __init__(self, activity_name: str) -> None:
        self.activity_name = activity_name