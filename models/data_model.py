import pandas as pd
from pathlib import Path

from services.svg_parser import SVGParser


class DataModel(object):
    headers = [
        "индекс",
        "Первичная формулировка",
        "Внешняя / Внутренняя",
        "Классификация проблеммы",
        "Бизнесс процесс",
        "Вид биснесс процесса",
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

        self.df = pd.read_csv(self.filename)
        self.df = self.df.fillna(' ')

    def load_from_svg(self, filename):
        self.filename = Path(filename[:-3] + 'csv')
        result = SVGParser(filename).result
        column_num = len(self.headers)
        df = pd.DataFrame(result, columns=[self.headers[0], self.headers[1]])
        for i in range(2, column_num):
            df.insert(len(df.columns), self.headers[i], value='')

        df[[self.headers[0]]] = df[[self.headers[0]]].apply(pd.to_numeric)
        df = df.sort_values(self.headers[0])
        self.df = df


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
