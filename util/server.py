import socket
from typing import Callable
from util.request import Request

class Server(object):
    __server: socket.socket
    __enabled: bool
    __routes: Callable[[Request], None]

    def __init__(self, host: str, port: int) -> None:
        self.__enabled = True

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((host, port))

    def listen(self) -> None:
        self.__server.listen()

        while self.__enabled:
            client_sock, _ = self.__server.accept()
            client = Request(client_sock)
            self.__bind_path(client)
            

    def __bind_path(self, request: Request):
        self.__routes(request)

    def bind_route(self, routes: Callable[[Request], None]):
        self.__routes = routes