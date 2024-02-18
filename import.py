
import pandas as pd
import mysql.connector

# Read the Excel file into a DataFrame
csv_file = 'WIPRO.csv'
df = pd.read_csv(csv_file)

# Establish a connection to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="nitesh",
    password="root@123",
    database="stocks"
)
cursor = db_connection.cursor()

# Define the MySQL query to insert data into the database table
insert_query = "INSERT INTO stock_prices (Symbol, Date, Open_Price, High_Price, Low_Price, Close_Price) VALUES (%s, %s, %s, %s, %s, %s)"

# Iterate over the rows of the DataFrame and insert each row into the database table
for index, row in df.iterrows():
    data = (row['Symbol'], row['Date'], row['Open Price'], row['High Price'], row['Low Price'], row['Close Price'])
    cursor.execute(insert_query, data)

# Commit the changes and close the cursor and database connection
db_connection.commit()
cursor.close()
db_connection.close()
