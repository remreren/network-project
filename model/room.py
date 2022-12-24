from typing import List

class Room(object):
    room_name: str
    reserved: dict[int, List[int]]

    def __init__(self, room_name: str, reserved: dict[int, List[int]] = {}) -> None:
        self.room_name = room_name
        self.reserved = reserved

    def is_available(self, day: int, hour: int, duration: int) -> bool:
        already_reserved = self.reserved.get(day)

        if already_reserved == None:
            already_reserved = []

        needed_hours = range(hour, hour + duration)        
        intersected_hours = list(set(already_reserved) & set(needed_hours))

        return len(intersected_hours) == 0

    def reserve(self, day: int, hour: int, duration: int) -> bool:
        if not self.is_available(day, hour, duration):
            return False
        
        already_reserved = self.reserved[day]
        needed_hours = range(hour, hour + duration)
        self.reserved[day] = list(set(already_reserved).union(set(needed_hours)))

        return True
