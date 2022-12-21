from model.database import Database, CustomEncoder
from model.reservation import Reservation
from util.request import Request
from util.server import Server
from repo.activity_repo import ActivityRepository
from model.activity import Activity
import json

server = Server("localhost", 8082)
database: Database = Database("./activities.json")

def get(request: Request):
    
    if (request.get_path().startswith("/add")):
        success = database.add_activity(Activity(request.get_query_param("name")))
        request.send_response(200 if success else 403, "activity added successfully" if success else "activity already exists")
    
    elif (request.get_path().startswith("/getall")):
        request.send_response(200, json.dumps({"activities": database.activities}, cls=CustomEncoder))

    elif (request.get_path().startswith("/remove")):
        request.send_response(200, "activity removed")
    
    elif (request.get_path().startswith("/check")):
        request.send_response(200, "activity")
    
    else:
        request.send_response(500, "route error")

def routes(request: Request):

    if (request.get_method() == "GET"):
        get(request)

    else:
        request.send_response(500, "method not supported")

server.bind_route(routes)
server.listen()


