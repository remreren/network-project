import socket
from typing import Callable
from util.request import Request

class Server(object):
    __server: socket.socket
    __enabled: bool
    __routes: dict[tuple[str, str], Callable[[dict, dict], tuple[int, str]]]
    __error_path: Callable[[str, str], tuple[int, str]]

    def __init__(self, host: str, port: int) -> None:
        self.__enabled = True
        self.__routes = {}

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((host, port))

    def listen(self) -> None:
        self.__server.listen()

        while self.__enabled:
            client_sock, _ = self.__server.accept()
            client = Request(client_sock)
            self.__call_path(client.get_method(), client.get_path(), client)

    def __call_path(self, method: str, path: str, client: Request):
        method_to_run = self.__routes.get((method, path))
        if method_to_run == None:
            status, result = self.__error_path(method, path)
        
        else:
            status, result = method_to_run(client.get_query_params(), client.get_body())
            
        client.send_response(status, result)

    def bind_path(self, method: str, path: str, runnable: Callable[[dict, dict], tuple[int, str]]):
        self.__routes[(method, path)] = runnable
    
    def error_path(self, runnable: Callable[[dict, dict], tuple[int, str]]):
        self.__error_path = runnable

    def bind_route(self, routes: Callable[[Request], None]):
        self.__routes = routes