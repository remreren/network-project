import json
from model.database import CustomEncoder, Database
from model.room import Room
from util.request import Request
from util.server import Server

server = Server("localhost", 8081)
database = Database("./database.json")

def get(request: Request):

    if (request.get_path().startswith("/add")):
        room_name = request.get_query_param("name")
        if room_name == None:
            request.send_response(400, "invalid request")
            return
           
        success = database.add_room(Room(room_name))
        if not success:
            request.send_response(403, f"room already exits with name {room_name}")
            return

        request.send_response(200, "new room added successfully")
        return
    
    elif (request.get_path().startswith("/remove")):
        room_name = request.get_query_param("name")
        if room_name == None:
            request.send_response(400, "invalid request")
            return
           
        success = database.remove_room(room_name)
        if not success:
            request.send_response(403, f"room cannot be found with name {room_name}")
            return

        request.send_response(200, "room deleted successfully")
        return

    elif (request.get_path().startswith("/reserve")):
        # name, day, hour, duration required
        room_name = request.get_query_param("name")
        day = int(request.get_query_param("day"))
        hour = int(request.get_query_param("hour"))
        duration = int(request.get_query_param("duration"))

        if room_name == None:
            request.send_response(400, "bad request")
            return
        
        room = database.get_room(room_name)
        available = room.is_available(day, hour, duration)

        if not available:
            request.send_response(403, "not available")
            return

        success = database.reserve_room(day, hour, duration)
        if not success:
            request.send_response(403, "reservation not done")
            return

        request.send_response(200, "reserved successfully")
        return
    
    elif (request.get_path().startswith("/checkavailability")):
        room_name = request.get_query_param("name")
        day = int(request.get_query_param("day"))
        hour = int(request.get_query_param("hour"))
        duration = int(request.get_query_param("duration"))

        if room_name == None:
            request.send_response(400, "bad request")
            return
        
        room = database.get_room(room_name)
        available = room.is_available(day, hour, duration)

        if not available:
            request.send_response(403, "not available")
            return

        request.send_response(200, "available")
        return
    
    elif (request.get_path().startswith("/getall")):
        request.send_response(200, json.dumps({"rooms": database.get_rooms()}, cls=CustomEncoder))
    
    else:
        request.send_response(500, "route error")

def routes(request: Request):
    
    if (request.get_method() == "GET"):
        get(request)

    else:
        request.send_response(500, "method not supported")

server.bind_route(routes)
server.listen()
