from flask import Flask
from flask_restful import Resource, Api
from flask_mysqldb import MySQL
from secrets import secrets

app = Flask(__name__)
s = secrets()

# https://flask-mysqldb.readthedocs.io/en/latest/
app.config['MYSQL_HOST'] = s.host
app.config['MYSQL_USER'] = s.user
app.config['MYSQL_PASSWORD'] = s.dBpw
app.config['MYSQL_DB'] = 'ardoinodata'

api = Api(app)
mysql = MySQL(app)


def writeIntoDB(temp, hum, date):
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO arduinodata VALUES (%d, %d, %s)", (temp, hum, date))
        mysql.connection.commit()
        cur.close()
        return "db writing success"
    except:
        return "db writing failed"


class MyData(Resource):
    def get(self, temp, hum, date):
        status = writeIntoDB(temp, hum, date)
        return {"job": {"temp": temp, "hum": hum, "date": date}, "status": status}


# Data should come as fill:temp=1,hum=1,date=1
api.add_resource(MyData, '/fill:temp=<int:temp>,hum=<int:hum>,date=<int:date>')

if __name__ == '__main__':
    app.run(debug=True)
