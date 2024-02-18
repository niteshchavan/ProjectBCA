import numpy as np
import mysql.connector
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
from decimal import Decimal


def fetch_data(symbol):
    # Connect to MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="nitesh",
        password="root@123",
        database="stocks"
    )
    cursor = db_connection.cursor()

    # Fetch x_train and y_train from the database for the given symbol
    cursor.execute("SELECT Open_Price, High_Price, Low_Price, Close_Price FROM stock_prices WHERE Symbol = %s", (symbol,))
    data = cursor.fetchall()

    # Close database connection
    cursor.close()
    db_connection.close()

    # Convert data to suitable Python data types
    data = [(float(row[0]), float(row[1]), float(row[2]), float(row[3])) for row in data]

    return data


def prepare_data(data):
    # Exludes last element (Close_Price) from the data
    x_train = np.array([row[:-1] for row in data])
    # Extracts only the Close_Price, which is the 4th element in each row
    y_train = np.array([row[3] for row in data])

    return x_train, y_train


def build_model(input_shape):
    # Define a simple Sequential model
    model = Sequential([
        Dense(64, activation='relu', input_shape=input_shape),  # Input shape based on number of features
        Dense(32, activation='relu'),
        Dense(1)  # Output layer with linear activation function for regression
    ])

    # Compile the model
    model.compile(optimizer='adam',
                  loss='mean_squared_error',  # Mean squared error loss for regression
                  metrics=['mae'])  # Mean absolute error metric

    return model


def train_model(model, x_train, y_train):
    # Train the model
    model.fit(x_train, y_train, epochs=10, batch_size=32)  # Adjust batch size as needed

    return model


def save_model(model, filename):
    # Save the model
    model.save(filename)
    print("Model Data Saved")


# List of stock symbols
symbols = ["TCS", "ITC", "WIPRO"]

# Train a separate model for each symbol
for symbol in symbols:
    print(f"Training model for symbol: {symbol}")
    data = fetch_data(symbol)
    x_train, y_train = prepare_data(data)
    model = build_model(input_shape=(x_train.shape[1],))
    model = train_model(model, x_train, y_train)
    save_model(model, f'{symbol}_model')
