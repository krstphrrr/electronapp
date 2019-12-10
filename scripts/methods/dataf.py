import pandas as pd
class df:
    def __init__(self, in_df):
        if in_df.endswith('.csv'):
            self.csv_to_df = in_df
        else:
            self.path_to_df = in_df

    def csv(self):
        self.df_csv = pd.read_csv(self.in_df)
        return self.df_csv
