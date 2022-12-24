from model.database import Database
from util.server import Server

server = Server("localhost", 8080)
database = Database("./database.json")

def add_reservation(query_params: dict, body: dict) -> tuple[int, str]:
    return (200, "activity added successfully")

def remove_reservation(query_params: dict, body: dict) -> tuple[int, str]:
    return (200, "activity removed")

def check_reservation(query_params: dict, body: dict) -> tuple[int, str]:
    return (200, "activity")

def error(path: str, method: str) -> tuple[int, str]:
    return (500, f"path {path} with method {method} cannot be found")

server.bind_path("GET", "/add", add_reservation)
server.bind_path("GET", "/remove", remove_reservation)
server.bind_path("GET", "/check", check_reservation)

server.error_path(error)

server.listen()
