from model.activity import Activity
from model.reservation import Reservation
from model.room import Room
from typing import List
import json

class Database(object):
    activities: List[Activity]
    reservations: List[Reservation]
    rooms: List[Room]

    __file_path: str

    def __init__(self, file_path: str) -> None:
        self.activities = []
        self.reservations = []
        self.rooms = []
        self.__file_path = file_path

        self.read()

    def add_activity(self, activity: Activity) -> bool:
        self.read()

        if activity.activity_name in map(lambda act: act.activity_name, self.activities):
            return False
        
        self.activities.append(activity)
        self.save()
        return True

    def remove_activity(self, activity_name: str) -> bool:
        self.read()

        activity = next(filter(lambda act: act.activity_name == activity_name, self.activities), None)

        if activity == None:
            return False

        self.activities.remove(activity)
        self.save()
        return True        

    def add_reservation(self, reservation: Reservation) -> bool:
        self.read()

        if reservation in self.reservations:
            return False
        
        self.reservations.append(reservation)
        self.save()
        return True

    def add_room(self, room: Room) -> bool:
        self.read()

        if room.room_name in map(lambda rm: rm.room_name, self.rooms):
            return False

        self.rooms.append(room)
        self.save()
        return True

    def get_room(self, room_name: str) -> Room:
        self.read()
        room = next(filter(lambda rm: rm.room_name == room_name, self.rooms), None)
        return room
    
    def remove_room(self, room_name: str) -> bool:
        self.read()

        room = next(filter(lambda room: room.room_name == room_name, self.rooms), None)
        if room == None:
            return False

        self.rooms.remove(room)
        self.save()
        return True

    def get_activities(self) -> List[Activity]:
        self.read()
        return self.activities

    def get_rooms(self) -> List[Room]:
        self.read()
        return self.activities

    def save(self) -> bool:
        with open(self.__file_path, "w+") as fl:
            fl.write(json.dumps(self, cls=CustomEncoder))

    def read(self) -> None:
        try:
            with open(self.__file_path, "r") as fl:
                data = json.load(fl)
                self.activities = [self.decode_activity(act) for act in data["activities"]]
                self.reservations = [self.decode_reservation(res) for res in data["reservations"]]
                self.rooms = [self.decode_room(room) for room in data["rooms"]]
        except Exception:
            self.activities = []
            self.reservations = []
            self.rooms = []

            self.save()

    def decode_activity(self, act_dct: dict) -> Activity:
        return Activity(act_dct["activity_name"])

    def decode_reservation(self, res_dct: dict) -> Reservation:
        return Reservation(int(res_dct["reservation_hour"]), int(res_dct["reservation_day"]), res_dct["reservation_room"])

    def decode_room(self, room_dct: dict) -> Room:
        return Room(room_dct["room_name"], room_dct["reserved"])


class CustomEncoder(json.JSONEncoder):

    def default(self, o: object) -> dict:
        if isinstance(o, List):
            return [item for item in o]
            
        elif isinstance(o, object):
            return {filtered_attr: getattr(o, filtered_attr) for filtered_attr in filter(lambda attr: not attr.startswith("_") and not callable(getattr(o, attr)), [attr for attr in dir(o)])}

        return json.JSONEncoder.default(self, o)