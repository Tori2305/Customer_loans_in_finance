import psycopg2
import pandas as pd
import numpy as np
import yaml

with open('credentials.yaml','r') as file:
    credentials=yaml.safe_load(file)

conn = psycopg2.connect(
    host=credentials['RDS_HOST'],
    port=credentials['RDS_PORT'],
    database=credentials['RDS_DATABASE'],
    user=credentials['RDS_USER'],
    password=credentials['RDS_PASSWORD'])

cursor = conn.cursor()
conn.close()