import json
import psycopg2
from psycopg2 import sql

# Step 1: Read the JSON file into Python
json_file_name = 'forecast_data.json'

# Read the JSON file
with open(json_file_name, 'r') as json_file:
    data_dict = json.load(json_file)

# Step 2: Connect to your PostgreSQL database
def connect_to_db():
    # Database connection details (replace with your actual credentials)
    conn = psycopg2.connect(
        dbname='Hackathon',
        user='postgres',
        password='1904',
        host="localhost",  # or use the server IP
        port="5432"        # default PostgreSQL port
    )
    return conn

# Step 3: Insert data into the PostgreSQL database
def insert_data_into_db(data):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Step 3.1: Define your SQL insert query
    insert_query = """
    INSERT INTO forecast (Symbol, Name, Country, Date, Type, Forecast1, ForecastDate1, Forecast2, ForecastDate2, Forecast3, ForecastDate3, Forecast4, ForecastDate4)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Step 3.2: Iterate over the data_dict and insert each record into the table
    for record in data:
        values = (
            record.get('Symbol'),
            record.get('Name'),
            record.get('Country'),
            record.get('Date'),
            record.get('Type'),
            record.get('Forecast1'),
            record.get('ForecastDate1'),
            record.get('Forecast2'),
            record.get('ForecastDate2'),
            record.get('Forecast3'),
            record.get('ForecastDate3'),
            record.get('Forecast4'),
            record.get('ForecastDate4')
        )
        cursor.execute(insert_query, values)

    # Step 3.3: Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

# Step 4: Upload the data to the database
insert_data_into_db(data_dict)
print("Data uploaded to the database successfully.")
