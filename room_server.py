import json
from model.database import CustomEncoder, Database
from model.room import Room
from util.http_request import create_response
from util.server import Server

server = Server("localhost", 8081)
database = Database("./database.json")

def add_room(query_params: dict, body: dict) -> tuple[int, str]:
    room_name = query_params.get("name")
    if room_name == None:
        return create_response(400, "Error", "Invalid request")
        
    success = database.add_room(Room(room_name))
    if not success:
        return create_response(403, "Error", f"room already exits with name {room_name}")

    return create_response(200, "Room added", "New room added successfully")

def remove_room(query_params: dict, body: dict) -> tuple[int, str]:
    room_name = query_params.get("name")
    if room_name == None:
        return create_response(400, "Error", "Invalid request")
        
    success = database.remove_room(room_name)
    if not success:
        return create_response(403, "Error", f"room cannot be found with name {room_name}")

    return create_response(200, "Delete room", "Room deleted successfully")

def reserve_room(query_params: dict, body: dict) -> tuple[int, str]:
    room_name = query_params.get("name")
    day = int(query_params.get("day"))
    hour = int(query_params.get("hour"))
    duration = int(query_params.get("duration"))

    if room_name == None:
        return create_response(400, "Error", "Bad request")
    
    room = database.get_room(room_name)
    available = room.is_available(day, hour, duration)

    if not available:
        return create_response(403, "Error", "Not available")

    success = database.reserve_room(room_name, day, hour, duration)
    if not success:
        return create_response(403, "Error", "Reservation not done")

    return create_response(200, "Reserve room", "Reserved successfully")

def check_availability(query_params: dict, body: dict) -> tuple[int, str]:
    room_name = query_params.get("name")
    day = query_params.get("day")

    if room_name == None:
        return create_response(400, "Error", "Bad request")
    
    room = database.get_room(room_name)
    if room == None:
        return create_response(404, "Error", "Room not found")

    if day == None:
        availabilities = room.get_all_availabilities()
        availabilities_widx = [(key, list(filter(lambda it: it[1], [(idx, value) for idx, value in enumerate(availabilities.get(key))]))) for key in availabilities.keys()]
        availabilities_by_days = [(day, "".join(map(lambda av: f"<li>{av[0]:02d}:00</li>", avs))) for day, avs in availabilities_widx]
        availabilities_final = "".join(map(lambda av: f"<li>Day {av[0]}<ul>{av[1]}</ul></li>", availabilities_by_days))
        
        return create_response(200, "Room availabilities", availabilities_final)
    
    else:
        availabilities = room.get_availabilities(day)
        availabilities_widx = list(filter(lambda it: it[1], [(idx, value) for idx, value in enumerate(availabilities)]))
        availabilities_final = "".join(map(lambda item: f"<li>{item[0]}</li>", availabilities_widx))

        if len(availabilities_widx) == 0:
            return create_response(403, "Error", "No availability for the room")

        return create_response(200, "Room availabilities", availabilities_final)

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
