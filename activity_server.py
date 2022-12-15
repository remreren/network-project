from util.request import Request
from util.server import Server

server = Server("localhost", 8082)

def get(request: Request):
    
    if (request.get_path().startswith("/add")):
        request.send_response(200, "activity added successfully")
    
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
