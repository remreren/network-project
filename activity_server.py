from model.database import Database, CustomEncoder
from util.request import Request
from util.server import Server
from model.activity import Activity
import json

server = Server("localhost", 8082)
database = Database("./database.json")

def get(request: Request):
    
    if (request.get_path().startswith("/add")):
        activity_name = request.get_query_param("name")
        
        if activity_name == None:
            request.send_response(400, "bad request")
            return

        success = database.add_activity(Activity(activity_name))
        if not success:
            request.send_response(403, "activity already exists")
            return

        request.send_response(200, "activity added successfully")
        return

    elif (request.get_path().startswith("/remove")):
        activity_name = request.get_query_param("name")
        
        if activity_name == None:
            request.send_response(400, "bad request")
            return

        success = database.remove_activity(Activity(activity_name))
        if not success:
            request.send_response(403, "activity does not exists")
            return

        request.send_response(200, "activity removed successfully")
        return

    elif (request.get_path().startswith("/check")):
        request.send_response(200, "activity")
    
    elif (request.get_path().startswith("/getall")):
        request.send_response(200, json.dumps({"activities": database.get_activities()}, cls=CustomEncoder))
    
    else:
        request.send_response(500, "route error")

def post(request: Request):
    
    if (request.get_path().startswith("/add")):
        activity_name = request.get_body()["name"]
        
        if activity_name == None:
            request.send_response(400, "bad request")
            return

        success = database.add_activity(Activity(activity_name))
        if not success:
            request.send_response(403, "activity already exists")
            return

        request.send_response(200, "activity added successfully")
        return

    elif (request.get_path().startswith("/remove")):
        activity_name = request.get_body()["name"]
        
        if activity_name == None:
            request.send_response(400, "bad request")
            return

        success = database.remove_activity(Activity(activity_name))
        if not success:
            request.send_response(403, "activity does not exists")
            return

        request.send_response(200, "activity removed successfully")
        return

    elif (request.get_path().startswith("/check")):
        request.send_response(200, "activity")
    
    elif (request.get_path().startswith("/getall")):
        request.send_response(200, json.dumps({"activities": database.get_activities()}, cls=CustomEncoder))
    
    else:
        request.send_response(500, "route error")

def routes(request: Request):

    if (request.get_method() == "GET"):
        get(request)

    elif (request.get_method() == "POST"):
        post(request)

    else:
        request.send_response(500, "method not supported")

server.bind_route(routes)
server.listen()


