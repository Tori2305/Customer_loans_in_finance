from db_utils import *

#Extracting all I need from the previous code to test before adding into it:
connector = RDSDatabaseConnector(credentials)
engine=connector.initialize_engine()
df = connector.extract_loan_payments()

print(f"Percentage of nulls: {df['mths_since_last_record'].isnull().sum()/len(df)}")
