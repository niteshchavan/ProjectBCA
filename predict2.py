import numpy as np
import mysql.connector
from tensorflow.keras.models import load_model
from decimal import Decimal


# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="nitesh",
    password="root@123",
    database="stocks"
)
cursor = db_connection.cursor()

# Fetch list of all symbols
cursor.execute("SELECT DISTINCT Symbol FROM stock_prices")
symbols = [row[0] for row in cursor.fetchall()]

# Close cursor
cursor.close()

# Close database connection
db_connection.close()

# Dictionary to store predicted close prices for each symbol
predicted_close_prices = {}

# Load the trained model for each symbol and make predictions
for symbol in symbols:
    # Connect to MySQL database and retrieve latest data for the symbol
    db_connection = mysql.connector.connect(
        host="localhost",
        user="nitesh",
        password="root@123",
        database="stocks"
    )
    cursor = db_connection.cursor()
    cursor.execute(f"SELECT Open_Price, High_Price, Low_Price, Close_Price FROM stock_prices WHERE Symbol = '{symbol}' ORDER BY Date DESC LIMIT 1")
    latest_data = cursor.fetchone()
    cursor.close()
    db_connection.close()

    # Convert decimal.Decimal values to float
    latest_data = [float(val) if isinstance(val, Decimal) else val for val in latest_data]

    # Load the trained model
    model = load_model(f'{symbol}_model')

    # Make a prediction for the next day's Close Price
    x_input = np.array([latest_data[:-1]])  # Exclude the Close_Price from the input data
    predicted_close_price = model.predict(x_input)

    # Store the predicted close price for the symbol
    predicted_close_prices[symbol] = predicted_close_price[0][0]

# Print predicted close prices for each symbol
for symbol, close_price in predicted_close_prices.items():
    print(f"Predicted Close Price for {symbol}: {close_price}")
