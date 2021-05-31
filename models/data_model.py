import pandas as pd
from pathlib import Path

from services.svg_parser import SVGParser


class DataModel(object):
    headers = [
        "индекс",
        "Первичная формулировка",
        "Внешняя / Внутренняя",
        "Классификация проблеммы",
        "Бизнес процесс",
        "Вид биснес процесса",
        "З.Г.Д."
    ]

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataModel, cls).__new__(cls)
        return cls.instance

    def _create_empty_data(self):
        problems = []
        self.df = pd.DataFrame(problems, columns=self.headers)
        self.add_empty_row()

    def load_from_csv(self, filename):
        self.filename = Path(filename)
        try:
            self.df = pd.read_csv(self.filename)
        except Exception as e:
            print(f'open csv {e}')
        self.df = self.df.fillna(' ')
        self.sort_by_index()

    def load_from_svg(self, filename):
        self.filename = Path(filename[:-3] + 'csv')
        result = SVGParser(filename).result
        column_num = len(self.headers)
        df = pd.DataFrame(result, columns=[self.headers[0], self.headers[1]])
        for i in range(2, column_num):
            df.insert(len(df.columns), self.headers[i], value='')

        self.df = df
        self.sort_by_index()


    def new_table(self):
        self.filename = Path().cwd() / 'новая таблица.csv'
        self._create_empty_data()

    def add_empty_row(self):
        try:
            self.df = self.df.append(pd.DataFrame([['']*self.df.shape[1]], columns=self.headers), ignore_index=True)
            self.df.iloc[self.df.shape[0]-1, 2] = 'Внутренняя'
        except Exception as e:
            print(e)

    def delete_row(self, row_num: int):
        self.df.drop(labels=row_num, inplace=True)
        self.df = self.df.reset_index(drop=True)

    def get_html_from_df(self):
        return self.df.to_html()

    def sort_by_index(self):
        df = self.df
        try:
            df[[self.headers[0]]] = df[[self.headers[0]]].apply(pd.to_numeric)
            df.sort_values(self.headers[0], kind='mergesort', inplace=True, ignore_index=True)
        except Exception as e:
            print(f'data model {e}')
        self.df = df