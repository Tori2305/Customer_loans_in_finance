import pandas as pd

df = pd.df = pd.read_csv("loan_payments.csv")


class DataTransform:
    def __init__ (self, df):
        self.df = df

    def categorical_cols(self):
        categorical_columns = ['purpose', 'grade', 'home_ownership', 'verification_status', 'loan_status']
        for col in categorical_columns:
            if col in self.df.columns:  # Check if the column exists
                self.df[col] = pd.Categorical(self.df[col])
            else:
                print(f"Column '{col}' not found in DataFrame.")

    def datetime_cols(self):
        datetime_columns = ['issue_date', 'last_payment_date', 'next_payment_date', 'earliest_credit_line', 'last_credit_pull_date']
        for col in datetime_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col])
            else:
               print(f"Column '{col}' not found in DataFrame.")

    def timedelta_cols(self):
        timedelta_columns = ['mths_since_last_delinq','mths_since_last_record']
        for col in timedelta_columns:
            if col in self.df.columns:
                self.df[col]=pd.to_timedelta(self.df[col])
            else:
                print(f"Column '{col}' not found in DataFrame.")

    def get_dataframe(self):
        return self.df
    
transformer = DataTransform(df)
transformer.timedelta_cols()
transformer.datetime_cols()
transformer.categorical_cols()
print(transformer.df.info())
