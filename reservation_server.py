from model.database import Database
from util.http_request import send_request, create_response
from util.server import Server

server = Server("localhost", 8080)
database = Database("./database.json")

def make_reservation(query_params: dict, body: dict) -> tuple[int, str]:
    room_name = query_params.get("room")
    activity_name = query_params.get("activity")
    day = int(query_params.get("day"))
    hour = int(query_params.get("hour"))
    duration = int(query_params.get("duration"))
    
    if room_name == None or activity_name == None:
        return create_response(400, "Error", "Input is invalid")

    activity_status, _ = send_request("GET", f"localhost:8081/check?name={activity_name}", {})
    if activity_status != 200:
        return create_response(activity_status, "Error", "Activity is not found")

    reservation_status, _ = send_request("GET", f"localhost:8082/reserve?name={room_name}&day={day}&hour={hour}&duration={duration}")
    if reservation_status == 403:
        return create_response(reservation_status, "Error", "Room does not exists of not available")

    return create_response(200, "Reservation created", "Reservation created successfully")

def list_availability(query_params: dict, body: dict) -> tuple[int, str]:
    room_name = query_params.get("room")
    day = query_params.get("day")

    if day != None:
        status, body = send_request("GET", f"localhost:8081/checkavailability?name={room_name}&day={day}", {})

    else:
        status, body = send_request("GET", f"localhost:8081/checkavailability?name={room_name}", {})
    
    return (status, body)

def display_reservation(query_params: dict, body: dict) -> tuple[int, str]:
    return (200, "activity")

def error(path: str, method: str) -> tuple[int, str]:
    return (500, f"path {path} with method {method} cannot be found")


server.bind_path("GET", "/reserve", make_reservation)
server.bind_path("GET", "/listavailability", list_availability)
server.bind_path("GET", "/display", display_reservation)

server.error_path(error)

server.listen()
