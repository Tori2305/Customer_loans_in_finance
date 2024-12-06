import pandas as pd

df = pd.df = pd.read_csv("loan_payments.csv")
print(df.info())

class DataTransform:
    def __init__ (self,df):
        self.df = df

    def convert_to_string(self, column_name, format=None, errors = 'raise'):
        
