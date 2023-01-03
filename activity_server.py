from model.database import Database, CustomEncoder
from util.http_request import create_response
from util.server import Server
from model.activity import Activity
import json

server = Server("localhost", 8082)
database = Database("./database.json")

def add_activity_post(query_params: dict, body: dict) -> tuple[int, str]:
    activity_name = body.get("name")
        
    if activity_name == None:
        return create_response(400, "Error", "bad request")

    success = database.add_activity(Activity(activity_name))
    if not success:
        return create_response(403, "Error", "activity already exists")

    return create_response(200, "Activity added", "activity added successfully")

def remove_activity_post(query_params: dict, body: dict) -> tuple[int, str]:
    activity_name = body.get("name")
    
    if activity_name == None:
        return create_response(400, "Error", "bad request")

    success = database.remove_activity(Activity(activity_name))
    if not success:
        return create_response(403, "Error", "activity does not exists")

    return create_response(200, "Activity removed", "activity removed successfully")

def add_activity(query_params: dict, body: dict) -> tuple[int, str]:
    activity_name = query_params.get("name")
    
    if activity_name == None:
        return create_response(400, "Error", "bad request")

    success = database.add_activity(Activity(activity_name))
    if not success:
        return create_response(403, "Error", "activity already exists")

    return create_response(200, "Activity added", "activity added successfully")

def remove_activity(query_params: dict, body: dict) -> tuple[int, str]:
    activity_name = query_params.get("name")
    
    if activity_name == None:
        return create_response(400, "Error", "bad request")

    success = database.remove_activity(Activity(activity_name))
    if not success:
        return create_response(403, "Error", "Activity does not exists")

    return create_response(200, "Activity removed", "Activity removed successfully")

def check_activity(query_params: dict, body: dict) -> tuple[int, str]:
    activity_name = query_params.get("name")

    if activity_name == None:
        return create_response(400, "Error", "bad request")
    
    if database.get_activity(activity_name) == None:
        return create_response(403, "Error", "Activity not found")
    
    return create_response(200, "Activity availability", "Activity exists")

def get_all_activities(query_params: dict, body: dict) -> tuple[int, str]:
    return create_response(200, "All activities", json.dumps({"activities": database.get_activities()}, cls=CustomEncoder))

def error(path: str, method: str) -> tuple[int, str]:
    return create_response(500, "Not found", f"path {path} with method {method} cannot be found")

server.bind_path("GET", "/add", add_activity)
server.bind_path("GET", "/remove", remove_activity)
server.bind_path("GET", "/check", check_activity)
server.bind_path("GET", "/getall", get_all_activities)

server.bind_path("POST", "/add", add_activity_post)
server.bind_path("POST", "/remove", remove_activity_post)
server.bind_path("POST", "/getall", get_all_activities)

server.error_path(error)

server.listen()


