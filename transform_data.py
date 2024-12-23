import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm

from scipy.stats import normaltest, zscore, boxcox, skew
from statsmodels.graphics.gofplots import qqplot


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

#Milestone3 - Task 2
class DataFrameInfo: 
    def __init__ (self, df):
         self.df = df
    
    def describe (self):
        """Describes all columns in the dataframe"""
        print(self.df.info())
    
    def statistical_values(self):
        """Extracts, median, standard deviation and mean for all dtype that include a number"""
        for col in self.df.select_dtypes(include=['number']):
            print(f"\n Column: {col}" )
            print(f"  Median: {self.df[col].median()}")
            print(f"  Standard Deviation: {self.df[col].std()}")
            print(f"  Mean: {self.df[col].mean()}")

    def distinct_values(self):
        """Extracts the distinct values within each column in the dataframe"""
        result = {}
        for col in self.df.columns:
            if self.df[col].dtype in ['category', 'object']:  # Only consider categorical or object columns
                result[col] = self.df[col].nunique()
        return result
              
    def shape (self):
        """Prints the shape of the dataframe"""
        df_rows=self.df.shape[0]
        df_columns=self.df.shape[1]
        print(" ")
        print(f"Total number of rows: {df_rows}")
        print(f"Total number of columns: {df_columns}")

    def null_counts(self):
        """Produces new table which returns all columns which have null values"""
        null_counts = self.df.isnull().sum()
        null_cols = null_counts[null_counts > 0] 
         
        if not null_cols.empty:
            null_percentages = (null_cols / len(self.df)) * 100
            print("\n")
            null_info = pd.DataFrame({'Null Count': null_cols, 'Null Percentage': null_percentages})
            print(null_info)
        else:
            print("No columns with null values found.")

class DataFrameTransform():
    def __init__ (self, df):
        self.df = df

    def null_counts(self):
        """Produces new table which returns all columns which have null values"""
        null_counts = self.df.isnull().sum()
        null_cols = null_counts[null_counts > 0] 
        
        if not null_cols.empty:
            null_percentages = (null_cols / len(self.df)) * 100
            # Return the result as a DataFrame with both count and percentage
            null_info = pd.DataFrame({'Null Count': null_cols, 'Null Percentage': null_percentages})
            return null_info
        else:
            return "No columns with null values found."

    def remove_high_null_columns(self):
        """
        Remove the four columns with the highest % of missing data.
        """
        columns_to_drop = [
            "mths_since_last_record", "mths_since_last_major_derog", 
            "next_payment_date", "mths_since_last_delinq"
        ]
        #print(f"Attempting to drop columns: {columns_to_drop}")
        self.df = self.df.drop(columns=columns_to_drop, axis=1, errors='ignore')
        #print("Columns after dropping:", self.df.columns)
        return self.df

    def impute_columns_with_median(self):
        for col in ['int_rate','funded_amount']:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(self.df[col].median())
        return self.df

    def impute_columns_with_mode(self):
        if 'term' in self.df.columns:
            mode_value = self.df['term'].mode()[0]
            self.df['term']=self.df['term'].fillna(mode_value)
        return self.df

    def remove_rows_with_missing_data(self):
        rows_to_drop = ['employment_length','collections_12_mths_ex_med','last_credit_pull_date','last_payment_date']
        self.df= self.df.dropna(subset=rows_to_drop, how = 'any')
        return self.df
    
    def identify_skewed_columns(self, df, columns):
        skew_cols = df[columns].apply(lambda x: skew(x.dropna()))

        highly_skewed_cols = []
        moderate_skewed_cols = []
        acceptable_skewed_cols = []

        for col, skew_value in skew_cols.items():
            if skew_value > 2:
                #print(f"Column '{col}' has a high skewness: {skew_value}. Consider transformation.")               
                highly_skewed_cols.append(col)
            elif skew_value > 1:
                #print(f"Column '{col}' has moderate skewness: {skew_value}. May require review.")
                moderate_skewed_cols.append(col)
            else:
                #print(f"Column '{col}' has acceptable skewness: {skew_value}.")
                acceptable_skewed_cols.append(col)
            
        print(f"Highly skewed cols: {highly_skewed_cols}")
        print(f"Moderatley skewed cols: {moderate_skewed_cols}")
        print(f"Acceptable skewed cols: {acceptable_skewed_cols}")

        return highly_skewed_cols, moderate_skewed_cols, acceptable_skewed_cols
    
    def transform_data_based_on_skewness (self, df, columns):
        highly_skewed_cols, moderate_skewed_cols, acceptable_skewed_cols = self.identify_skewed_columns(df, columns)

        for col in highly_skewed_cols:
            print(f"Applying log transformation to: {col}")
            df[col] = np.log1p(df[col]) 

        for col in moderate_skewed_cols:
            print(f"Applying square root transformation to: {col}")
            df[col] = np.sqrt(df[col])

        return df
    
    def remove_outliers(self,df,columns):
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)

            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
            print(f"Lower bound: {lower_bound}, Upper bound: {upper_bound}")

        return df 
    
    def drop_columns(self, df, columns_to_drop):
        df_dropped = df.drop(columns=columns_to_drop, errors='ignore')
        
        print(f"Dropped columns: {columns_to_drop}")
        return df_dropped

    def get_updated_dataframe(self):
       return self.df


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

    def visualising_column_distribution(self, df, new_df, column):
        if isinstance(column,str):
            column = [column]

        for col in column:
            plt.figure(figsize=(10,5))
            plt.subplot(1,2,1)
            df[col].dropna().hist(bins=30)
            plt.title(f'Original {col}')

            plt.subplot(1, 2, 2)
            np.log1p(df[col]).dropna().hist(bins=30)
            plt.title(f'Log Transformed: {col}')

            plt.show()
   

    def boxplot_columns(self, df, column):
        """Generate boxplots for numeric columns to visualize outliers."""
        for col in column:
            if pd.api.types.is_numeric_dtype(df[col]):
                plt.figure(figsize=(8, 5))
                plt.boxplot(df[col].dropna(), vert=False)
                plt.title(f"Boxplot for {col}")
                plt.xlabel(col)
                plt.show()
            else:
                print(f"Skipping column '{col}': Not numeric.")

    def comparison_of_data(self, df, new_df, columns):
        for col in columns:
            plt.figure(figsize=(20, 10))
        
            # Before removing outliers: Boxplot for all columns
            plt.subplot(1, 2, 1)
            sns.boxplot(data=df[col])  # Assuming 'numerical_columns' is your list of columns
            plt.title(f"Boxplot Before Removing Outliers - {col}")
            plt.xticks(rotation=90)


            # After removing outliers: Boxplot for all columns
            plt.subplot(1, 2, 2)
            sns.boxplot(data=new_df[col])  # 'cleaned_df' is your DataFrame after removing outliers
            plt.title(f"Boxplot After Removing Outliers - {col}")
            plt.xticks(rotation=90)

        plt.tight_layout()
        plt.show()

