import numpy as np
import mysql.connector
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Connect to MySQL database and retrieve data
db_connection = mysql.connector.connect(
    host="localhost",
    user="nitesh",
    password="root@123",
    database="stocks"
)

cursor = db_connection.cursor()
cursor.execute("SELECT Open_Price, High_Price, Low_Price, Close_Price FROM stock_prices")
data = cursor.fetchall()
cursor.close()
db_connection.close()

# Convert data to suitable Python data types and prepare features and target variable
data = [(float(row[0]), float(row[1]), float(row[2]), float(row[3])) for row in data]
x_train = np.array([row[:-1] for row in data])  # Features
y_train = np.array([row[3] for row in data])    # Target variable

# Normalize the data
scaler = MinMaxScaler()
x_train_normalized = scaler.fit_transform(x_train)

# Define and train an XGBoost model
xgb_model = XGBRegressor()
xgb_model.fit(x_train_normalized, y_train)

# Make predictions using the trained XGBoost model
x_input = np.array([data[-1][:-1]])  # Use the latest data point for prediction
predicted_close_price_xgb = xgb_model.predict(scaler.transform(x_input))

# Print predicted close prices
print("Predicted Close Price (XGBoost):", predicted_close_price_xgb[0])
