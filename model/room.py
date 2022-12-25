from typing import List

class Room(object):
    room_name: str
    reserved: dict[int, List[int]]

    def __init__(self, room_name: str, reserved: dict[int, List[int]] = {}) -> None:
        self.room_name = room_name
        self.reserved = reserved
    
    def get_availabilities(self, day: int) -> List[bool]:
        already_reserved = self.reserved.get(day)

        if already_reserved == None:
            already_reserved = []
        
        availabilities = [True] * 24
        for i in already_reserved:
            availabilities[i] = False

        return availabilities
    
    def get_all_availabilities(self) -> dict[int, List[bool]]:
        return {day: self.get_availabilities(day) for day in range(1, 8)}

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
        
        already_reserved = self.reserved.get(day)
        if already_reserved == None:
            already_reserved = []

        needed_hours = range(hour, hour + duration)
        self.reserved[day] = list(set(already_reserved).union(set(needed_hours)))

        return True
