import pandas as pd
from os.path import join


class Select_tbl:
    """

    """
    temp_table = None
    @staticmethod
    def __init__(self,in_df, *vals, field = None):
        self.in_df = in_df
        self.field = field
        self.vals = vals
        dfset = []

        def name(arg1,arg2):
            self.arg1 = arg1
            self.arg2 = arg2
            return join(self.arg1, self.arg2)

        if all(self.in_df):
            try:
                for val in self.vals:
                    index = self.in_df[f'{self.field}']==f'{val}'
                    exec('%s = self.in_df[index]' % name(f'{self.field}',f'{val}'))
                    dfset.append(eval(name(f'{self.field}',f'{val}')))

                self.temp_table = pd.concat(dfset)
            except Exception as e:
                print(e)
        else:
            print('error')

    # def __invert__(self):
    #     oppositeindex = self.in_df[f'{self.field}']==f'{val}'
    #     self.temp_table = self.in_df[~oppositeindex]
    #     return self.temp_table
