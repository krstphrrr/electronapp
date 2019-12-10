# from dataf import df
from os import listdir,getcwd, chdir
from os.path import normpath, join
from utils import Acc
import pandas as pd

class Table:
    temp=None
    def __init__(self,in_table=None, path=None):
        self.path = path
        self.in_table = in_table
        con = Acc(self.path).con
        query = f'SELECT * FROM "{self.in_table}"'
        self.temp = pd.read_sql(query,con)

    def temp(self):
        return self.temp
