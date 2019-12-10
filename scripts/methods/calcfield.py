import pandas as pd
#
# df1 = pd.DataFrame({'a':['one','two'],
#                     'b':['three','four'],
#                     'c':['five','six']})
#
#
# calc = calcField()
# calc.comb(df1,'MYFIELD','a','b','c')

class calc:

    def __init__(self,*arg,**args):
        self.arg = arg
        self.args = args

    def comb(self,in_df,newfield,*fields):
        self.in_df = in_df
        self.newfield = newfield
        self.fields = fields

        self.in_df[f'{self.newfield}'] = (self.in_df[[f'{field}' for field in self.fields]].astype(str)).sum(axis=1)
        return self.in_df
