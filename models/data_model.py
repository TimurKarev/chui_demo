import pandas as pd
from pathlib import Path


from services.parse_svg import SVGParser


class DataModel(object):
    headers = [
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

    # def __init__(self):
    #     self.df = pd.DataFrame()
    #     self._create_empty_data()
    #     self.filename = Path().cwd() / 'new_file.csv'

    def _create_empty_data(self):
        problems = []
        self.df = pd.DataFrame(problems, columns=[self.headers])

    def load_from_csv(self, filename):
        self.filename = filename
        self.filename = Path(self.filename)

        self.df = pd.read_csv(filename)
        self.df = self.df.fillna(' ')

    def load_from_svg(self, filename):
        self.filename = filename[:-3] + 'csv'
        self.filename = Path(self.filename)

        problems = SVGParser.parse_svg(filename)
        column_num = len(self.headers)
        df = pd.DataFrame(problems, columns=[self.headers[0]])
        for i in range(1, column_num):
            df.insert(len(df.columns), self.headers[i], value='')
        self.df = df

    def new_table(self, filename):
        self.filename = filename + '.csv'
        self.filename = Path(self.filename)

        self._create_empty_data()

