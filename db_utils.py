import psycopg2
import pandas as pd
import yaml
from sqlalchemy import create_engine

class RDSDatabaseConnector:
    '''
    A class for connecting to and interacting with an RDS database

    Methods include initializing the database, establishing a 
    connection, extracting data, saving that data to a csv, 
    and closing the connection once complete.    
    '''

    def __init__(self,credentials:dict):
        '''
        Initilaizes the RDSDatabaseConnector with the provided credentials.
        '''   
        self.credentials = credentials
        self.conn = None
        self.engine = None    
    
    def connection (self):
        '''
        Initilizing a connection to the database and initializes the SQLAlchemy engine, 
        using info from yaml file.
        '''
        try:
            self.conn=psycopg2.connect(
                host=self.credentials['RDS_HOST'],
                port=self.credentials['RDS_PORT'],
                database=self.credentials['RDS_DATABASE'],
                user=self.credentials['RDS_USER'],
                password=self.credentials['RDS_PASSWORD']
            )
            print("PostgreSQL connection established successfully")
            
            engine_url = (f"postgresql://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}/{self.credentials['RDS_DATABASE']}")
            print("SQLAlchemy engine initialized successfully.")
            self.engine = create_engine(engine_url)
        except Exception as e:
            print(f"Error establishing connection or initializing engine: {e}")

    def extract_data(self, query:str):
        '''
        Executes a query and returns it as a Pandas database with the class taking a 
        SQL query as a string parameter.

        Testing to see if the connection has been made, if not response is to connect
        If connection then set up query of dataset from engine returning it as a new df
        If connection is set up but there is an error in extracting the data then error
        message will show
        '''
        if not self.engine:
            print("SQLAlchemy engine not initialized. Please call connect() first.")
            return pd.DataFrame()
        try:
            df = pd.read_sql_query(query, self.engine)
            print("Data extracted successfully")
            return df
        except Exception as e:
            print(f"Error extracting data: {e}")
            return pd.DataFrame()
    
    def save_data_to_csv(self, df:pd.DataFrame, filename: str ="data.csv"):
        """Saves the given DataFrame to a CSV file."""
        try:
            df.to_csv(filename, index=False)  # Set index=False to avoid saving row indices
            print(f"Data saved to {filename}")
            return filename # Return filepath for further use
        except Exception as e:
            print(f"Error saving data to CSV: {e}")
        
    def data_shape(self,df):
        '''Additional info looking at the shape of the data extracted via DataFrame'''
        print(df.shape)
        return df

    def disconnect(self):
      '''Closes connection if one exists'''
      if self.conn:
        self.conn.close()
        print("PostgreSQL connection is closed")
      else:
        print("No active connection to close.")
    
def load_credentials(filepath: str) -> dict:
    """
    Loads database credentials from a YAML file.
    """
    try:
        with open(filepath, "r") as file:
            credentials = yaml.safe_load(file)
            print("Credentials loaded successfully.")
            return credentials
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return {}

if __name__ == "__main__":
    credentials = load_credentials("credentials.yaml")

    connector = RDSDatabaseConnector(credentials)
    connector.connection()
    
    query = "SELECT * FROM loan_payments"
    data = connector.extract_data(query)

    if not data.empty:
        connector.save_data_to_csv(data,filename="loan_payments.csv")
    
    connector.disconnect()