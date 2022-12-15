import socket
from request_parser import RequestParser

class Request(object):
    __client: socket.socket
    __parser: RequestParser
    __headers: dict

    def __init__(self, client: socket.socket) -> None:
        self.__client = client
        self.__parser = RequestParser(client.recv(8192).decode())
        self.__headers = {}

    def send_response(self, status: int, body: str) -> None:
        response = ""
        response += f"HTTP/1.1 {status} OK\r\n"

        self.__headers["Content-Length"] = len(body)
        self.__headers["Content-Type"] = "text/html"

        for key in self.__headers.keys():
            response += f"{key}: {self.__headers[key]}\r\n"

        response += "\r\n"
        response += body

        self.__client.send(response.encode())
        self.__client.close()

    def add_header(self, key: str, value: object) -> None:
        self.__headers[key] = value

    def get_parser(self) -> RequestParser:
        return self.__parser