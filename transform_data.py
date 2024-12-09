import pandas as pd

df = pd.df = pd.read_csv("loan_payments.csv")

#Milestone3 - Task 1
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

#Milestone3 - Task 2
class DataFrameInfo: 
    def __init__ (self,df):
         self.df = df
    
    def describe (self):
        """Describes all columns in the dataframe"""
        print(self.df.info())
    
    def statistical_values(self):
        """Extracts, median, standard deviation and mean for all dtype that include a number"""
        for col in self.df.select_dtypes(include=['number']):
            print(f"Column: {col}" )
            print(f"  Median: {self.df[col].median()}")
            print(f"  Standard Deviation: {self.df[col].std()}")
            print(f"  Mean: {self.df[col].mean()}")

    def distinct_values(self):
        """Extracts the distinct values within each column within the datafram"""
        for col in self.df.columns: 
            if self.df[col].dtype in ['category']:
                print(f"{col} has: {self.df[col].nunique()} values")
              
    def shape (self):
        """Prints the shape of the dataframe"""
        shape_of_dataframe = self.df.shape
        print(f"The shape of the dataframe is: {shape_of_dataframe}")

    def null_counts(self):
        """Produces new table which returns all columns which have null values"""
        null_counts = self.df.isnull().sum()
        null_cols = null_counts[null_counts > 0] 
         
        if not null_cols.empty:
            null_percentages = (null_cols / len(self.df)) * 100
            null_info = pd.DataFrame({'Null Count': null_cols, 'Null Percentage': null_percentages})
            print(null_info)
        else:
            print("No columns with null values found.")

describing = DataFrameInfo(df)
describing.describe()
describing.statistical_values()
describing.distinct_values()
describing.shape()
describing.null_counts()

