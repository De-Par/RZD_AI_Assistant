import os

import pandas as pd

from core.error_handler import raise_error
import pprint


class Parser(object):
    def __init__(self, file_pth: str) -> None:
        if not os.path.exists(file_pth):
            raise_error("0x000000")
        with open(file_pth, encoding='utf-8', mode='r') as file:
            self.data = self.__parse(file.readlines())


    @staticmethod
    def __parse(data: list) -> dict:
        res = {}
        while len(data) > 0:
            line = data.pop(0).strip()
            if len(line) == 0: continue
            if line.isdigit():
                defect = data.pop(0).strip()
                res[defect] = []
                while not data[0].strip().isdigit() and len(data) > 1:
                    reason = data.pop(0).strip()
                    method = data.pop(0).strip()
                    if reason + method == '':
                        continue
                    res[defect] += [(reason, method)]
        return res

    def to_pandas(self) -> pd.DataFrame:
        df = pd.DataFrame(columns=['Defect', 'Reason', 'Method'])
        for defect in self.data:
            for pair in self.data[defect]:
                df.loc[-1] = [defect, pair[0], pair[1]]
                df.index += 1
        return df
