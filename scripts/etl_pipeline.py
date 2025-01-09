import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Database credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# Encode the password if needed
from urllib.parse import quote
encoded_password = quote(DB_PASSWORD)

def load_cleaned_data(file_path,table_name):
    """loading cleaned data from csv intp postgres"""
    print("loading the data")

    df = pd.read_csv(file_path)
    print(f"Data preview: \n{df.head()}")

    # Correct connection string
    try:
        engine = create_engine(f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        connection = engine.connect()
        print("Connection successful!")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")


    df.to_sql(table_name,engine,if_exists='replace',index=False)
    print(f"Data loaded successfully into the '{table_name}' table!")

if __name__ == '__main__':
    file_path = '../data/clean_Product.csv'
    table_name = 'products'

     # Load the cleaned data into PostgreSQL
    load_cleaned_data(file_path, table_name)
