from flask import Flask, render_template, jsonify  
import numpy as np
import mysql.connector
from tensorflow.keras.models import load_model
from decimal import Decimal
import json
from datetime import datetime, timedelta

# Get today's date
today_date = datetime.today().strftime('%Y-%m-%d')


app = Flask(__name__)

@app.route('/data')

def index():
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

    # Dictionary to store historical and predicted prices for each symbol
    symbol_data = {}
    
    # Load the trained model for each symbol and make predictions
    for symbol in symbols:
        # Connect to MySQL database and retrieve historical data for the symbol
        db_connection = mysql.connector.connect(
            host="localhost",
            user="nitesh",
            password="root@123",
            database="stocks"
        )
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT Date, Open_Price, High_Price, Low_Price, Close_Price FROM stock_prices WHERE Symbol = '{symbol}' ORDER BY Date DESC Limit 14")

        historical_data = cursor.fetchall()

        cursor.close()
        db_connection.close()

        # Convert decimal.Decimal values to float
        #historical_data = [(val[0].strftime('%Y-%m-%d'),float(val[1]), float(val[2]), float(val[3])) if isinstance(val[0], datetime)val[1], Decimal) else val for val in historical_data]
        
        historical_data= [(row[0].strftime('%Y-%m-%d'), float(row[1]), float(row[2]), float(row[3])) for row in historical_data]
        #wait = input("Press Enter to continue.")
        #print(historical_data)
        # Load the trained model
        model = load_model(f'{symbol}_model')
        d1 = [data_point[0] for data_point in historical_data]
        
        #print(new_date_strings)
        # Make predictions for the next day's Close Price
        predicted_close_prices = []
        for data_point in historical_data:
            x_input = np.array([[data_point[1], data_point[2], data_point[3]]])  # Use historical close price as input

            predicted_close_price = model.predict(x_input)
            predicted_close_prices.append(float(predicted_close_price[0][0]))
            print([data_point[0], predicted_close_price[0][0]])
            #next_date = datetime.strptime(historical_dates[-1], '%Y-%m-%d') + timedelta(days=1)
            
        # Store historical and predicted prices for the symbol
        symbol_data[symbol] = {
            "dates": [data_point[0] for data_point in historical_data],
            "historical_prices": [data_point[1] for data_point in historical_data],
            "predicted_prices": predicted_close_prices,
            
            "predicted_date": [ (datetime.strptime(d1, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') for d1 in d1]
            
        }


    # Render HTML template with symbol data

    return jsonify(symbol_data)


@app.route('/')
def page():
    return render_template('chart.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
