from typing import List

class Room(object):
    room_name: str
    reserved: dict[List[int]]

    def __init__(self, room_name: str, reserved: dict[List[int]] = {}) -> None:
        self.room_name = room_name
        self.reserved = reserved