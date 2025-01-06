import psycopg2
import pandas as pd
import numpy as np
import yaml
from sqlalchemy import create_engine

with open('credentials.yaml','r') as file:
    credentials=yaml.safe_load(file)
    '''
    Read database connection details from the YAML file. 
    The safe_load function parses the YAML data so the python 
    code can use the details to connect to the database. 
    '''

class RDSDatabaseConnector:
    '''
    A class for connecting to and interacting with an RDS database

    Methods include initialising the database, establishing a 
    connection, extracting data, saving that data to a csv, 
    understanding the shape of it and closing the connection once complete.    
    '''

    def __init__(self,credentials):
        self.credentials = credentials
        self.conn = None
        self.engine = None    
        '''
        Initilaizes the RDSDatabaseConnector with no active connection
        '''

    def initialize_engine(self):
        '''
        Initilaizing the database engine for connection
        '''
        engine_url = (f"postgresql://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}/{self.credentials['RDS_DATABASE']}")
        self.engine = create_engine(engine_url)
        print("SQLAlchemy engine initialized successfully.")
        return self.engine
    
    def connection (self):
        '''
        Initilizing a connection using info from the YAML file (credentials)
        '''
        self.conn=psycopg2.connect(
            host=self.credentials['RDS_HOST'],
            port=self.credentials['RDS_PORT'],
            database=self.credentials['RDS_DATABASE'],
            user=self.credentials['RDS_USER'],
            password=self.credentials['RDS_PASSWORD'])
        

    def extract_loan_payments(self):
        '''
        Testing to see if the connection has been made, if not response is to connect
        If connection then set up query of dataset from engine returning it as a new df
        If connection is set up but there is an error in extracting the data then error
        message will show
        '''
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
        '''Looking at the shape of the data extracted via DataFrame'''
        print(df.shape)
        return df

    def disconnect(self):
      '''Closes connection if one exists'''
      if self.conn:
        self.conn.close()
        print("PostgreSQL connection is closed")
      else:
        print("No active connection to close.")

if __name__ == "__main__":
    connector = RDSDatabaseConnector(credentials)
    connector.connection()
    engine=connector.initialize_engine()
    df = connector.extract_loan_payments()
    df_shape = connector.load_data_to_df(df)
    file_path=connector.save_data_to_csv(df)
    connector.disconnect()