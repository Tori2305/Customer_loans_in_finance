import psycopg2 # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
import yaml # type: ignore
from sqlalchemy import create_engine # type: ignore

with open('credentials.yaml','r') as file:
    credentials=yaml.safe_load(file)

class RDSDatabaseConnector:
    def __init__(self,credentials):
        self.credentials = credentials
        self.conn = None
        self.engine = None    

    def initialize_engine(self):
        engine_url = (f"postgresql://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}/{self.credentials['RDS_DATABASE']}")
        self.engine = create_engine(engine_url)
        print("SQLAlchemy engine initialized successfully.")
        return self.engine
    
    def connection (self):
        self.conn=psycopg2.connect(
            host=self.credentials['RDS_HOST'],
            port=self.credentials['RDS_PORT'],
            database=self.credentials['RDS_DATABASE'],
            user=self.credentials['RDS_USER'],
            password=self.credentials['RDS_PASSWORD'])
        self.engine = self.initialize_engine()

    def extract_loan_payments(self):
        if not self.engine:
            print("SQLAlchemy engine not initialized. Please call connect() first.")
            return None
        try:
            query = "SELECT * FROM loan_payments" 
            df = pd.read_sql_query(query, self.engine)
            return df
        except Exception as e:
            print(f"Error extracting data: {e}")
            return None
    
    def save_data_to_csv(self, df, filename="loan_payments.csv"):
        """Saves the given DataFrame to a CSV file."""
        try:
            df.to_csv(filename, index=False)  # Set index=False to avoid saving row indices
            print(f"Data saved to {filename}")
            return filename # Return filepath for further use
        except Exception as e:
            print(f"Error saving data to CSV: {e}")
            return None
        
    def load_data_to_df(self,df):
        print(df.shape)
        return df

    def disconnect(self):
      if self.conn:
        self.conn.close()
        print("PostgreSQL connection is closed")
      else:
        print("No active connection to close.")


connector = RDSDatabaseConnector(credentials)
engine=connector.initialize_engine()
df = connector.extract_loan_payments()
df_shape = connector.load_data_to_df(df)
file_path=connector.save_data_to_csv(df)
print(f'File saved at: {file_path}')
connector.disconnect()