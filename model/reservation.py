class Reservation(object):
    reservation_id: str
    reservation_hour: int
    reservation_day: int
    reservation_room: str
    
    def __init__(self, reservation_id: str, reservation_hour: int, reservation_day: int, reservation_room: str) -> None:
        self.reservation_id = reservation_id
        self.reservation_hour = reservation_hour
        self.reservation_day = reservation_day
        self.reservation_room = reservation_room