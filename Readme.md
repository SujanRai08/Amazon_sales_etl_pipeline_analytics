# ETL Pipeline for Sales Data Analytics
# Data is taken from kaggle with amazon_sales_data

### Project Overview
This project focuses on building an ETL (Extract,Transform, Load) pipeline that processes sales data,performs data cleaning and transformation, and loads the final dataset into a PostgreSQL database for analytical reporting.

### 1. Project Setup 
*Pre-requisities*
- Python 3.x installed.
- PostgreSQL installed and configured.
- Required Python libraries:
    - pandas
    - sqlalchemy
    - psycopg2
    - numpy
### Steps to Set Up the Environment:
1. Create a virtual environment (optional but recommended):
```python
python -m venv etl_project_env
```
2. Activate the virtual environment:
- On Windows:
  ```python
  etl_project_env/Scripts/activat.bat
  ```
3. Install the required libraries:
   ```python
   pip install pandas sqlalchemy psycopg2 numpy matplotlib
   ```

### 2. Extract (Data Loading)
*Data source*
The initial dataset is extracted from a CSV file containing raw sales data. The file has several columns including product details, sales data, and review content.
```python
import pandas as pd
# Load the data from CSV
data = pd.read_csv("sales_data.csv")
```

### 3. Transform (Data Cleaning and Processing)
*3.1 Data Cleaning*
Data cleaning was done to ensure that the data is structured, consistent, and free of errors. This process includes:

- Handling Missing Values: Columns with null values were either filled with appropriate defaults or removed.
- Removing Irrelevant Columns: Columns such as review_id, review_title, and review_content were removed due to the data being irrelevant to the analysis.
- Splitting Product Descriptions: The about_product field contains multiple pieces of information separated by the | symbol, which was split into separate columns for better analysis.

```python
data.drop(['review_id', 'review_title', 'review_content'], axis=1, inplace=True)
data['about_product'] = data['about_product'].str.split('|', expand=True)
data.fillna('Unknown', inplace=True)
```

*3.2 Data Transformation*
The transformation step involved applying specific business rules, such as calculating discounts and ensuring that product pricing was aligned with the discount percentage.
```python
# Calculate the discounted price if not present
data['discounted_price'] = data['actual_price'] - (data['actual_price'] * (data['discount_percentage'] / 100))
```

### 4.  Load (Inserting Data into PostgreSQL)
*4.1 Setup PostgreSQL database*
- Install PostgreSQL and set up a database. For example, create a database named sales_data_db.
- Ensure your PostgreSQL server is running and accessible.

*4.2 Database Connection*
You will connect to PostgreSQL using SQLAlchemy and psycopg2. Here’s how to establish a connection:
```python
from sqlalchemy import create_engine
username = 'your_username'
password = 'your_password'
database_name = 'sales_data_db'
engine = create_engine(f'postgresql+psycopg2://{username}:{password}@localhost/{database_name}')
```

*4.3 Create Table*
You can create a table in PostgreSQL to store the cleaned data using SQLAlchemy or directly via SQL commands. If using SQLAlchemy, it will automatically map the DataFrame to the database table.
```python
data.to_sql('sales_data', engine, if_exists='replace', index=False)
```

*4.4 Verify Data in PostgreSQL*
Once the data is loaded, run the following SQL query in your PostgreSQL client to ensure the data was successfully inserted:
```python
SELECT * FROM sales_data LIMIT 10;
```

### 5.  Add Testing and Error Handling:
To check whether the project is running successfully or not. Ensure, try and expect is placed correctly.
```python
try:
    engine = create_engine(f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Error: {e}")
```


### 6.  Running the ETL pipeline:

To run the ETL pipeline, execute the Python script. This script will:

1. Extract the data from the CSV file.
2. Clean and transform the data (removing unnecessary columns, handling missing values, splitting text, etc.).
3. Load the transformed data into PostgreSQL.
```python
python etl_pipeline.py
```

### 7. Analtyics and Reporting:
Once the data is in PostgreSQL, you can begin creating analytical reports. For example, you can create queries to get the total sales per category, products with the highest ratings, or analyze discounts.

```sql
-- Example: Total Sales by Category
SELECT category_level_1, SUM(discounted_price) AS total_sales
FROM sales_data
GROUP BY category_level_1;
```

### 7. Future Enhancements
- Automate the ETL pipeline using tools like Apache Airflow or Prefect.
- Create visual dashboards using tools like Power BI or Tableau.
- Advance error handling and logging in the pipeline.


### 8. Conclusion
This project successfully demonstrates how to build an ETL pipeline to process and load sales data into PostgreSQL for reporting and analytics. With a clean and structured dataset, it's now possible to generate valuable business insights from the sales data.

