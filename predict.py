import numpy as np
import mysql.connector
from tensorflow.keras.models import load_model
from decimal import Decimal


# Connect to MySQL database and retrieve latest data

db_connection = mysql.connector.connect(
    host="localhost",
    user="nitesh",
    password="root@123",
    database="stocks"
)

cursor = db_connection.cursor()
cursor.execute("SELECT Open_Price, High_Price, Low_Price, Close_Price FROM stock_prices ORDER BY Date DESC LIMIT 1")
latest_data = cursor.fetchone()
cursor.close()
db_connection.close()


# Convert decimal.Decimal values to float
latest_data = [float(val) if isinstance(val, Decimal) else val for val in latest_data]

#print(latest_data)
#wait = input("Press Enter to continue.")


# Load the trained model
model = load_model('my_model')

# Make a prediction for the next day's Close Price
x_input = np.array([latest_data[:-1]])  # Exclude the Close_Price from the input data


predicted_close_price = model.predict(x_input)

print("Predicted Close Price for the next day:", predicted_close_price)
