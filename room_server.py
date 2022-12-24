import json
from model.database import CustomEncoder, Database
from model.room import Room
from util.server import Server

server = Server("localhost", 8081)
database = Database("./database.json")

def add_room(query_params: dict, body: dict) -> tuple[int, str]:
    room_name = query_params.get("name")
    if room_name == None:
        return (400, "invalid request")
        
    success = database.add_room(Room(room_name))
    if not success:
        return (403, f"room already exits with name {room_name}")

    return (200, "new room added successfully")

def remove_room(query_params: dict, body: dict) -> tuple[int, str]:
    room_name = query_params.get("name")
    if room_name == None:
        return (400, "invalid request")
        
    success = database.remove_room(room_name)
    if not success:
        return (403, f"room cannot be found with name {room_name}")

    return (200, "room deleted successfully")

def reserve_room(query_params: dict, body: dict) -> tuple[int, str]:
    room_name = query_params.get("name")
    day = int(query_params.get("day"))
    hour = int(query_params.get("hour"))
    duration = int(query_params.get("duration"))

    if room_name == None:
        return (400, "bad request")
    
    room = database.get_room(room_name)
    available = room.is_available(day, hour, duration)

    if not available:
        return (403, "not available")

    success = database.reserve_room(day, hour, duration)
    if not success:
        return (403, "reservation not done")

    return (200, "reserved successfully")

def check_availability(query_params: dict, body: dict) -> tuple[int, str]:
    room_name = query_params.get("name")
    day = int(query_params.get("day"))
    hour = int(query_params.get("hour"))
    duration = int(query_params.get("duration"))

    if room_name == None:
        return (400, "bad request")
    
    room = database.get_room(room_name)
    available = room.is_available(day, hour, duration)

    if not available:
        return (403, "not available")

    return (200, "available")

def get_all(query_params: dict, body: dict) -> tuple[int, str]:
    return (200, json.dumps({"rooms": database.get_rooms()}, cls=CustomEncoder))

def error(path: str, method: str) -> tuple[int, str]:
    return (500, f"path {path} with method {method} cannot be found")

server.bind_path("GET", "/add", add_room)
server.bind_path("GET", "/remove", remove_room)
server.bind_path("GET", "/reserve", reserve_room)
server.bind_path("GET", "/checkavailability", check_availability)
server.bind_path("GET", "/getall", get_all)

server.error_path(error)

server.listen()
