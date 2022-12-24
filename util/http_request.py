import socket
import json

def send_request(method: str, link: str, body: dict) -> str:
    request = ""

    authority, path = link.split("/", 1)
    host, port = authority.split(":", 1)
    ip = socket.gethostbyname(host)

    request += f"{method} /{path} HTTP/1.1\r\n"
    request += f"Host: {authority}\r\n\r\n"
    request += json.dumps(body)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((ip, int(port)))
    server_sock.send(bytes(request, encoding="UTF-8"))
    response = server_sock.recv(8192)

    return parse_status(str(response))

def parse_status(response: str) -> int:
    status = response.splitlines()[0].split()[1]
    return int(status)