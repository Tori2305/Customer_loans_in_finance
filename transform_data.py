import pandas as pd
from scipy.stats import normaltest, zscore
from statsmodels.graphics.gofplots import qqplot
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm

df = pd.df = pd.read_csv("loan_payments.csv")
print(df.info())

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

columns_to_exclude = ['id', 'member_id']
columns_to_check = [col for col in df.columns if col not in columns_to_exclude]

class DataFrameTransform():
    def null_counts(self, df):
        """Produces new table which returns all columns which have null values"""
        null_counts = df.isnull().sum()
        return df
     
    def remove_high_null_columns(self, df):
        """
        Remove the four columns with the highest % of missing data
        """
        columns_to_drop=['mths_since_last_record','mths_since_last_major_derog', 'next_payment_date', 'mths_since_last_delinq']
        df = df.drop(columns_to_drop, errors='ignore')
        return df

    def impute_columns_with_median(self, df):
        for col in ['int_rate','funded_amount']:
            if col in df.columns:
                df[col] =df[col].fillna(df[col]).median()
        return df

    def impute_columns_with_mode(self, df):
        if 'term' in df.columns:
            mode_value = df['term'].mode()[0]
            df['term']=df['term'].fillna(mode_value)
        return df

    def remove_rows_with_missing_data(self,df):
        rows_to_drop = ['employment_length','collections_12_mths_ex_med','last_credit_pull_date','last_payment_date']
        df= df.dropna(subset=rows_to_drop, how = 'any')
        return df
    
    def identify_skewed_columns(self, df, columns_to_check, skew_threshold=2.0):
        skewed_columns = {}
        for col in columns_to_check:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                skew_val = df[col].dropna().skew()
                if not np.isnan(skew_val) and abs(skew_val) > skew_threshold:
                    skewed_columns[col] = skew_val
            else:
                continue
        return skewed_columns

    def transform_columns(self, df, skewed_columns):
        transformed_df = df.copy()

        for col in skewed_columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                original_skew = df[col].dropna().skew()
                transformations =[
                    ('Log', (df[col] > 0).all(), np.log1p(df[col])),
                    ('Square Root', (df[col] >= 0).all(), np.sqrt(df[col])),
                    ('Box-Cox', (df[col] > 0).all(), stats.boxcox(df[col])[0] if (df[col] > 0).all() else df[col])
                ]
            
            best_skew, best_method, best_transformed_data = self.determine_best_skew(transformations, original_skew)
            transformed_df[col] = best_transformed_data
            print(f"Column '{col}': Original skew={original_skew:.2f}, Best transformation={best_method}, Skew after transformation={best_skew:.2f}")
            
        return transformed_df
            
    def determine_best_skew(self, transformations, original_skew):    
        best_skew = original_skew
        best_method = 'None'
        best_transformed_data = None

        for method, condition, transformed_data in transformations:
            if condition:
                skew_after_transformation = pd.Series(transformed_data).skew()  # Ensure it's a pandas series
                if abs(skew_after_transformation) < abs(best_skew):
                    best_skew = skew_after_transformation
                    best_method = method
                    best_transformed_data = transformed_data

        return best_skew, best_method, best_transformed_data
    
    def identify_outliers(self, df, skewed_columns):
        skewed_cols_list = list(skewed_columns.keys()) if isinstance(skewed_columns, dict) else skewed_columns
        df[skewed_cols_list] = df[skewed_cols_list].apply(pd.to_numeric, errors='coerce')
        df = df.dropna(subset=skewed_cols_list)
       
        z_scores_df = df[skewed_cols_list].apply(zscore)
        z_outliers = (z_scores_df.abs() > 3).any(axis=1)

        Q1 = df[skewed_cols_list].quantile(0.25)
        Q3 = df[skewed_cols_list].quantile(0.75)
        IQR = Q3 - Q1
        IQR_outliers = ((df[skewed_cols_list] < (Q1 - 1.5 * IQR)) | ((df[skewed_cols_list] > (Q3 + 1.5 * IQR))).any(axis=1))

        outliers_combined = z_outliers | IQR_outliers
        print(f"Number of rows identified as outliers using both methods:{outliers_combined.sum()}")

        return outliers_combined

transforming=DataFrameTransform()
df = transforming.null_counts(df)
new_df = transforming.remove_high_null_columns(df)
new_df = transforming.impute_columns_with_median(new_df)
new_df = transforming.impute_columns_with_mode(new_df)
new_df = transforming.remove_rows_with_missing_data(new_df)

columns_to_check = new_df.columns
skewed_columns = transforming.identify_skewed_columns(new_df,columns_to_check)
transformed_df = transforming.transform_columns(new_df,skewed_columns)

outliers = transforming.identify_outliers(transformed_df,skewed_columns)

print(outliers)

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
           
    def compare_column_distributions(self, original_df, transformed_df, columns):
        for col in columns:
            plt.figure(figsize=(18, 8))

            # Original Histogram
            plt.subplot(2, 2, 1)
            sns.histplot(original_df[col].dropna(), bins=30, kde=False, color='blue', alpha=0.6)
            plt.title(f"Original Histogram: {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")

            # Transformed Histogram
            plt.subplot(2, 2, 2)
            sns.histplot(transformed_df[col].dropna(), bins=30, kde=False, color='green', alpha=0.6)
            plt.title(f"Transformed Histogram: {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")

            # Original QQ Plot
            plt.subplot(2, 2, 3)
            sm.qqplot(original_df[col].dropna(), line='45', fit=True)
            plt.title(f"Original QQ Plot: {col}")

            # Transformed QQ Plot
            plt.subplot(2, 2, 4)
            sm.qqplot(transformed_df[col].dropna(), line='45', fit=True)
            plt.title(f"Transformed QQ Plot: {col}")

            plt.tight_layout()
            plt.show()
    

    def boxplot_columns(self, df, columns_to_check):
        """Generate boxplots for numeric columns to visualize outliers."""
        for col in columns_to_check:
            if pd.api.types.is_numeric_dtype(df[col]):
                plt.figure(figsize=(8, 5))
                plt.boxplot(df[col].dropna(), vert=False)
                plt.title(f"Boxplot for {col}")
                plt.xlabel(col)
                plt.show()
            else:
                print(f"Skipping column '{col}': Not numeric.")


#plotting = Plotter()
#plotting.plot_null_counts(df, new_df)
#plotting.compare_column_distributions(df, transformed_df, skewed_columns.keys())
#plotting.boxplot_columns(transformed_df, columns_to_check)

#new_df.to_csv('C:/Users/torig/Project_2/Customer_loans_in_finance/new_dataframe.csv', index=False)

