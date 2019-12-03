from flask import Flask
import pygal
import mysql.connector
from datetime import datetime, timedelta
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    try:
        cnx = mysql.connector.connect(user='dev0', password='Christa1',
                                      host='192.168.10.107', database='inetSpeed')  # 73.158.191.112

        cursor = cnx.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        past = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("SELECT datetime, speed_down, speed_up FROM inetLog WHERE datetime BETWEEN %s AND %s;",
                       (past, now))

        downData = list()
        upData = list()
        for i in cursor:
            downData.append((i[0], i[1]))
            upData.append((i[0], i[2]))

        line_chart = pygal.DateTimeLine(x_label_rotation=75,
                                        truncate_label=-1,
                                        x_value_formatter=lambda dt: dt.strftime('%m-%d %H:%M'))
        line_chart.add("Down", downData)
        line_chart.add("Up", upData)
        line_chart.render_to_png('chart.png')
        return line_chart.render_response()
    except Exception:
        return(str(Exception))


if __name__ == '__main__':
    app.run(debug=True)
