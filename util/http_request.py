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
    server_sock.send(request.encode("UTF-8"))
    response = server_sock.recv(8192)

    return parse_status(response.decode("UTF-8"))

def parse_status(response: str) -> tuple[int, str]:
    status = response.splitlines()[0].split()[1]
    _, body = response.split("\r\n\r\n", maxsplit=1)
    return (int(status), body)

def create_response(status: int, title: str, body: str) -> tuple[int, str]:
    return (status, f"""
<html>
    <head>
        <title>{title}</title>
    </head>
    <body>{body}</body>
</html>""")