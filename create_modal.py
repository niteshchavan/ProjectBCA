import numpy as np
import mysql.connector
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
from decimal import Decimal



# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="nitesh",
    password="root@123",
    database="stocks"
)
cursor = db_connection.cursor()

# Fetch x_train and y_train from the database

cursor.execute("SELECT Open_Price, High_Price, Low_Price, Close_Price FROM stock_prices")
data = cursor.fetchall()


# Convert data to suitable Python data types

data = [(float(row[0]), float(row[1]), float(row[2]), float(row[3])) for row in data]

x_train = np.array([row[:-1] for row in data])  # Exludes last element ie Close_Price from the data

y_train = np.array([row[3] for row in data])    # Extracting only the Close_Price, which is the 4th element in each row



# Close database connection
cursor.close()
db_connection.close()

# Define a simple Sequential model
model = Sequential([
    Dense(64, activation='relu', input_shape=(x_train.shape[1],)),  # Input shape based on number of features in x_train
    Dense(32, activation='relu'),
    Dense(1)  # Output layer with linear activation function for regression
])

# Compile the model
model.compile(optimizer='adam',
              loss='mean_squared_error',  # Mean squared error loss for regression
              metrics=['mae'])  # Mean absolute error metric


model.fit(x_train, y_train, epochs=10, batch_size=32)  # Adjust batch size as needed

# Save the model
model.save('my_model')

print("Model Data Saved")