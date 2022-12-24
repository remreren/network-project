from model.database import Database, CustomEncoder
from util.server import Server
from model.activity import Activity
import json

server = Server("localhost", 8082)
database = Database("./database.json")

def add_activity_post(query_params: dict, body: dict) -> tuple[int, str]:
    activity_name = body.get("name")
        
    if activity_name == None:
        return (400, "bad request")

    success = database.add_activity(Activity(activity_name))
    if not success:
        return (403, "activity already exists")

    return (200, "activity added successfully")

def remove_activity_post(query_params: dict, body: dict) -> tuple[int, str]:
    activity_name = body.get("name")
    
    if activity_name == None:
        return (400, "bad request")

    success = database.remove_activity(Activity(activity_name))
    if not success:
        return (403, "activity does not exists")

    return (200, "activity removed successfully")

def add_activity(query_params: dict, body: dict) -> tuple[int, str]:
    activity_name = query_params.get("name")
    
    if activity_name == None:
        return (400, "bad request")

    success = database.add_activity(Activity(activity_name))
    if not success:
        return (403, "activity already exists")

    return (200, "activity added successfully")

def remove_activity(query_params: dict, body: dict) -> tuple[int, str]:
    activity_name = query_params.get("name")
    
    if activity_name == None:
        return (400, "bad request")

    success = database.remove_activity(Activity(activity_name))
    if not success:
        return (403, "activity does not exists")

    return (200, "activity removed successfully")

def check_activity(query_params: dict, body: dict) -> tuple[int, str]:
    activity_name = query_params.get("name")

    if activity_name == None:
        return (400, "bad request")
    
    if database.get_activity(activity_name) == None:
        return (403, "activity not found")
    
    return (200, "activity")

def get_all_activities(query_params: dict, body: dict) -> tuple[int, str]:
    return (200, json.dumps({"activities": database.get_activities()}, cls=CustomEncoder))

def error(path: str, method: str) -> tuple[int, str]:
    return (500, f"path {path} with method {method} cannot be found")

server.bind_path("GET", "/add", add_activity)
server.bind_path("GET", "/remove", remove_activity)
server.bind_path("GET", "/check", check_activity)
server.bind_path("GET", "/getall", get_all_activities)

server.bind_path("POST", "/add", add_activity_post)
server.bind_path("POST", "/remove", remove_activity_post)
server.bind_path("POST", "/getall", get_all_activities)

server.error_path(error)

server.listen()


