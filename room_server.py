from util.request import Request
from util.server import Server

server = Server("localhost", 8081)

def get(request: Request):

    if (request.get_path().startswith("/add")):
        request.send_response(200, "new room added successfully")
    
    elif (request.get_path().startswith("/remove")):
        request.send_response(200, "room deleted successfully")

    elif (request.get_path().startswith("/reserve")):
        request.send_response(200, "reserved successfully")
    
    elif (request.get_path().startswith("/checkavailability")):
        request.send_response(200, "availability is set")
    
    else:
        request.send_response(500, "route error")

def routes(request: Request):
    
    if (request.get_method() == "GET"):
        get(request)

    else:
        request.send_response(500, "method not supported")

server.bind_route(routes)

server.listen()
