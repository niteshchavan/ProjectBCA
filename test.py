from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Configuration for MySQL connection




# Route to fetch data from MySQL and display as JSON
@app.route('/data')
def get_data():
    try:
        db_connection = mysql.connector.connect(
        host="localhost",
        user="nitesh",
        password="root@123",
        database="stocks"
        )
        cursor = db_connection.cursor()

        # Fetch list of all symbols
        cursor.execute("SELECT * FROM stock_prices")
        symbols = cursor.fetchall()

        # Close cursor
        cursor.close()

        # Close database connection
        db_connection.close()
        
        # Convert fetched data to JSON
        return jsonify(symbols)
    
    except Exception as e:
        return jsonify({'error': str(e)})
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
