from flask import Flask, request, json, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime, timezone
import requests
import os
import psycopg2
#database config


conn = psycopg2.connect(
        host="psql-service",
        database="flask_db",
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'))
cur = conn.cursor()
# in res= USD exchange rates , utctimes= UTC timestamp , curr = the target currency 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['POST'])
@cross_origin()
def index():
    cur.execute('CREATE TABLE IF NOT EXISTS currency (id serial PRIMARY KEY,target_curr varchar (150) NOT NULL, usd_ex decimal(18,6) NOT NULL,timestamp decimal(18,6) NOT NULL);')
    data = json.loads(request.data)
    curr = data['currency']
    response = requests.get("https://api.exchangerate.host/latest?base="+curr+"&symbols=USD")
    res= response.json()
    res = res['rates']['USD']
    date = datetime.now(timezone.utc)
    utct=date.replace(tzinfo=timezone.utc)
    utctimes=utct.timestamp()
    res_data={
        "res" : res,
        "timestamp" : utctimes
    }
    cur.execute("INSERT INTO currency (target_curr, usd_ex, timestamp) VALUES (%s, %s, %s);",(curr, res, utctimes))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(res_data)


if __name__ == "__main__":
    app.run(debug=True)
