import pandas as pd
from scipy.stats import normaltest
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
    
#transformer = DataTransform(df)
#transformer.timedelta_cols()
#transformer.datetime_cols()
#transformer.categorical_cols()

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
        df_rows=self.df.shape[0]
        df_columns=self.df.shape[1]
        print(f"Total number of rows: {df_rows}")
        print(f"Total number of columns: {df_columns}")

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

#describing = DataFrameInfo(df)
#describing.describe()
#describing.statistical_values()
#describing.distinct_values()
#describing.shape()
#describing.null_counts()

class DataFrameTransform():
    def null_counts(self, df):
        """Produces new table which returns all columns which have null values"""
        null_counts = df.isnull().sum()
        return df
     
    def remove_high_null_columns(self, df):
        """
        Remove the four columns with the highest % of missing data
        -mths_since_last_record
        -mths_since_last_major_derog
        - next_payment_date: Next scheduled payment date.
        - mths_since_last_delinq: The number of months since the last dealing.
        """
        df = df.drop(['mths_since_last_record','mths_since_last_major_derog', 'next_payment_date', 'mths_since_last_delinq'],axis=1)
        return df

    def impute_columns_with_median(self, df):
        df['int_rate'] =df['int_rate'].fillna(df['int_rate']).median()
        df['funded_amount'] =df['funded_amount'].fillna(df['funded_amount']).median()
        return df

    def impute_columns_with_mode(self, df):
        mode_value = df['term'].mode()[0]
        df['term']=df['term'].fillna(mode_value)
        return df

    def remove_rows_with_missing_data(self,df):
        df= df.dropna(subset=['employment_length','collections_12_mths_ex_med','last_credit_pull_date','last_payment_date'])
        return df
    
    def dataframe_new (self):
        return df

transforming=DataFrameTransform()
transforming.null_counts(df)
new_df = transforming.remove_high_null_columns(df)
new_df = transforming.impute_columns_with_median(new_df)
new_df = transforming.impute_columns_with_mode(new_df)
new_df = transforming.remove_rows_with_missing_data(new_df)
new_df = transforming.remove_rows_with_missing_data(new_df)


class Plotter ():
    """Class to visualise insights from the data""" 
    def plot_null_counts(self, df, new_df):
        df_nulls = df.isnull().sum()
        new_df_nulls= new_df.isnull().sum()
        null_data = pd.DataFrame({'Original DataFrame': df_nulls, 'New DataFrame': new_df_nulls})

        plt.figure(figsize=(20, 12))
        null_data.plot(kind='bar', colormap='viridis')

        plt.title('Null Values Before and After Transformation')
        plt.ylabel('Count of Null Values')
        plt.xlabel('Columns')
        plt.xticks(rotation=75)
        plt.show()

#plotting = Plotter()
#plotting.plot_null_counts(df, new_df)

new_df.to_csv('C:/Users/torig/Project_2/Customer_loans_in_finance/new_dataframe.csv', index=False)