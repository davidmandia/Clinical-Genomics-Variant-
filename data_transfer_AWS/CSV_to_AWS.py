import psycopg2
import configparser
import os

# Load the database configuration from the config file
config = configparser.ConfigParser()
config.read('data_transfer_AWS/db_config.ini')

# Connection details from the config file
host = config['postgresql']['host']
port = config['postgresql']['port']
database = config['postgresql']['database']
user = config['postgresql']['user']
password = config['postgresql']['password']

# Path to the cleaned CSV file
clean_csv_file_path = "/workspaces/Clinical-Genomics-Variant/output/database/GRCh38_indels_variant_clean.csv"

try:
    # Establishing the connection
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    
    # Create a cursor object
    cursor = connection.cursor()
    
    # Open the cleaned CSV file
    with open(clean_csv_file_path, 'r', encoding='utf-8') as f:
        cursor.copy_expert("COPY variants FROM STDIN WITH CSV HEADER", f)
    
    # Commit the changes
    connection.commit()
    
    print("CSV data imported successfully.")
    
    # Execute a simple query to verify the data
    cursor.execute("SELECT COUNT(*) FROM variants;")
    count_record = cursor.fetchone()
    print(f"Total records in variants table: {count_record[0]}")
    
    # Close the cursor and connection
    cursor.close()
    connection.close()
    
except Exception as error:
    print(f"Error while connecting to PostgreSQL: {error}")
