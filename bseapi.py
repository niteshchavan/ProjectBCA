from flask import Flask, render_template, jsonify, request
import mysql.connector
import requests

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="nitesh",
    password="root@123",
    database="stocks"
)



@app.route('/add', methods=['POST'])
def add():
    print("Inside /add route")
    if request.method == 'POST':
        data = request.json
        name = data.get('name')  # Get the 'name' field from the JSON data
        code = data.get('code')  # Get the 'code' field from the JSON data
        cursor = db.cursor()
        cursor.execute("INSERT INTO stocks_list(name, code) VALUES(%s, %s)", (name, code))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Data added successfully'})

@app.route('/delete/<int:id>', methods=['GET'])
def remove_data(id):
    cursor = db.cursor()
    # Remove data from the database based on data_id
    cursor.execute("DELETE FROM stocks_list WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Data deleted successfully'})



@app.route('/data')
def get_stock_data():
    url = "https://api.bseindia.com/BseIndiaAPI/api/getScripHeaderData/w"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Referer": "https://www.bseindia.com/",
    }
    
    cursor = db.cursor()
    cursor.execute("SELECT code from stocks_list")
    result = cursor.fetchall()
    cursor.close()
   
    script_codes = [str(row[0]) for row in result]
    print(script_codes)
    wait = input("Press Enter to continue.")
    tdata = []

    for script_code in script_codes:
        payload = {
            "Debtflag": "",
            "scripcode": script_code,
            "seriesid": "",
        }

        jsonData = requests.get(url, headers=headers, params=payload).json()

        stock_data = {}

        if "Cmpname" in jsonData:
            stock_data["Name"] = jsonData["Cmpname"]["ShortN"]

        if "CurrRate" in jsonData:
            stock_data["LTP"] = jsonData["CurrRate"]["LTP"]

        if "Header" in jsonData:
            stock_data["Previous_Close"] = jsonData["Header"]["PrevClose"]

        tdata.append(stock_data)

    return jsonify(tdata)


#@app.route('/stock_list')
#def stocklist():
#    sdata = []
#    cursor = db.cursor(dictionary=True)
#    cursor.execute("SELECT * FROM stocks_list")
#    sdata = cursor.fetchall()
#    cursor.close()
#    return jsonify(sdata)

@app.route('/stock_list')
def stocklist():
    sdata = []
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM stocks_list")
    for row in cursor:
        sdata.append(row)
    cursor.close()
    return jsonify(sdata)


@app.route('/')
def index():

    return render_template('ticker_tape2.html', )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
