from util.request import Request
from util.server import Server

server = Server("localhost", 9090)

def routes(request: Request):
    request.send_response(200, f"<h1> {request.get_method()} request done on path {request.get_path()} with query params {request.get_query_params()} </h1>")

server.bind_route(routes)

server.listen()
