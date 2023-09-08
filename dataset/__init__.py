import os
from core.error_handler import raise_error


class Parser(object):
    def __init__(self, file_pth: str) -> None:
        if not os.path.exists(file_pth):
            raise_error("0x000000")
        with open(file_pth, 'r') as file:
            data = file.read()

    @staticmethod
    def __parse(data: str) -> dict:
        res = {}


        return res


a = Parser()