from model.database import Database
from util.http_request import send_request
from util.server import Server

server = Server("localhost", 8080)
database = Database("./database.json")

def make_reservation(query_params: dict, body: dict) -> tuple[int, str]:
    # room, activity, day, hour, duration

    room_name = query_params.get("room")
    activity_name = query_params.get("activity")
    day = int(query_params.get("day"))
    hour = int(query_params.get("hour"))
    duration = int(query_params.get("duration"))

    activity_status = send_request("GET", f"localhost:8081/check?name={activity_name}", {})
    if activity_status != 200:
        return (activity_status, "activity status is not available")
    
    room_status = send_request("GET", f"127.0.0.1:8082/checkavailability?name={room_name}", {})
    if room_status != 200:
        return (room_status, "room status is not available")

    result = send_request("GET", f"localhost:8082/reserve?name={room_name}&")

    return (200, "activity added successfully")

def list_availability(query_params: dict, body: dict) -> tuple[int, str]:
    return (200, "activity removed")

def display_reservation(query_params: dict, body: dict) -> tuple[int, str]:
    return (200, "activity")

def error(path: str, method: str) -> tuple[int, str]:
    return (500, f"path {path} with method {method} cannot be found")

server.bind_path("GET", "/reserve", make_reservation)
server.bind_path("GET", "/listavailability", list_availability)
server.bind_path("GET", "/display", display_reservation)

server.error_path(error)

server.listen()
