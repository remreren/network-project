from typing import Tuple
import re
import json

class RequestParser(object):
    __method: str
    __raw_path: str
    __path: str
    __body: dict
    __query_params: dict

    def __init__(self, request: str) -> None:

        method, raw_path, path, query_params, body = self.__parse_request(request)

        self.__method = method
        self.__raw_path = raw_path
        self.__path = path
        self.__query_params = query_params
        self.__body = body

    # returns method, path, query_params and body respectively
    def __parse_request(self, request: str) -> Tuple[str, str, dict, dict]:
        headers, body_str = re.split("\r\n\r\n", request, maxsplit=1)
        method, raw_path, _ = re.split("\\s+", headers.splitlines()[0], maxsplit=2)

        path, query_params = self.__parse_path(raw_path)
        body = self.__parse_body(body_str)

        return (method, raw_path, path, query_params, body)

    def __parse_path(self, path: str) -> Tuple[str, dict]:
        splitted = re.split("\?", path)
        splitted_path = splitted[0].removesuffix("/")

        query_params = {}

        if len(splitted) > 1:
            entries = [re.split("=", entry) for entry in re.split("&", splitted[1])]
            query_params = {key.lstrip(): value.lstrip() for key, value in entries}

        return (splitted_path, query_params)

    def __parse_body(self, body: str) -> dict:
        if body == None or body.lstrip() == "":
            return {}
        return json.loads(body)

    def get_method(self) -> str:
        return self.__method

    def get_path(self) -> str:
        return self.__path

    def get_raw_path(self) -> str:
        return self.__raw_path
    
    def get_query_params(self) -> dict:
        return self.__query_params

    def get_body(self) -> dict:
        return self.__body