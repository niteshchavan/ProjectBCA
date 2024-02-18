from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# Function to fetch current stock prices from MySQL database
def fetch_stock_prices():
    # Connect to MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="nitesh",
        password="root@123",
        database="stocks"
    )
    cursor = db_connection.cursor(dictionary=True)
    try:
        with db_connection.cursor() as cursor:
            sql = """
                SELECT Symbol, Close_Price
                FROM stock_prices
                WHERE (Symbol, Date) IN (
                    SELECT Symbol, MAX(Date) AS Latest_Date
                    FROM stock_prices
                    GROUP BY Symbol
                )
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            
            return results
    finally:
        cursor.close()
        db_connection.close()

# Route to render the ticker tape template
@app.route('/')
def ticker_tape():
    # Fetch current stock prices
    stock_prices = fetch_stock_prices()
    print(stock_prices)
    #wait = input("Press Enter to continue.")
    return render_template('ticker_tape.html', stocks=stock_prices)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
