import os
import tqdm
import pandas as pd
import pickle

from core.error_handler import raise_error
from docx.api import Document

headers = [
    'тепловозах, 2М62, 2М62У',
    'тепловозах, 2ТЭ10М, 2ТЭ10МК, 2ТЭ10У, 2ТЭ10УК',
    'тепловозах, 2ТЭ25А',
    'тепловозах, 2ТЭ25КМ',
    'тепловозах, 2ТЭ70',
    'тепловозах, 2ТЭ116',
    'тепловозах, 2ТЭ116УД',
    'электровозах, 2ЭС4К',
    'электровозах, 2ЭС5К, 3ЭС5К',
    'электровозах, 2ЭС6',
    'электровозах, 2ЭС7',
    'электровозах, 2ЭС10',
    'электровозах, ВЛ10, ВЛ10У',
    'электровозах, ВЛ10К',
    'электровозах, ВЛ11, ВЛ11М',
    'электровозах, ВЛ11М',
    'электровозах, ВЛ15',
    'электровозах, ВЛ65',
    'электровозах, ВЛ80Р',
    'электровозах, ВЛ80С',
    'электровозах, ВЛ80Т',
    'электровозах, ВЛ85',
    'тепловозах, ТЭМ2',
    'тепловозах, ТЭМ7А',
    'тепловозах, ТЭМ14',
    'тепловозах, ТЭМ18Д, ТЭМ18ДМ',
    'тепловозах, ТЭП70',
    'тепловозах, ТЭП70БС',
    'тепловозах, ЧМЭ3',
    'электровозах, ЧС2',
    'электровозах, ЧС2К',
    'электровозах, ЧС2Т',
    'электровозах, ЧС4Т',
    'электровозах, ЧС6, ЧС200',
    'электровозах, ЧС7',
    'электровозах, ЧС8',
    'электровозах, ЭП1, ЭП1М',
    'электровозах, ЭП2К',
    'электровозах, ЭП10',
    'электровозах, ЭП20',
]


class TableParser(object):
    def __init__(self, data_path) -> None:
        if not os.path.exists(data_path):
            raise_error("0x000000")
        self.parse(data_path)

    @staticmethod
    def parse(data_path):
        dataframe = []
        document = Document(data_path)
        progress_bar = tqdm.tqdm(zip(headers, document.tables[1:]), desc='Parsing tables', total=len(headers))
        application = 0
        for header, table in progress_bar:
            application += 1
            rows = table.rows
            cells = [x.cells for x in rows]
            title = 'general'
            index_stack = [-1]
            for i, cell_row in enumerate(cells):
                row = [cell.text for cell in cell_row]
                # All the same string
                if all(row[0] == row[j] for j in range(len(row))):
                    if index_stack[-1] == i - 1:
                        title += '. ' + row[0]
                    else:
                        title = row[0]
                    index_stack.append(i)
                else:
                    temp = header.split(', ')
                    type_ = 'электровоз' if temp[0] == 'электровозах' else 'тепловоз'
                    series = temp[1:]
                    for s in series:
                        # Waste Rows
                        if row[1] in ('Неисправность', 'Неисправность(сообщение МПСУ)', 'Неисправность(сообщение МПСУиД)'):
                            continue
                        # Create link
                        link = f'Приложение N{application} П{row[0]}'
                        dataframe += [[type_, s, title, row[1], row[2], row[3], link]]
        dataframe = pd.DataFrame(dataframe, columns=['type', 'model', 'title', 'defect', 'reason', 'solution', 'link'])
        dataframe.to_excel('./dataset/parsed_data.xlsx')


TableParser('./dataset/original.docx')
