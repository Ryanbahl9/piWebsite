from flask import Flask
import pygal
import mysql.connector
from datetime import datetime, timedelta
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    try:
        cnx = mysql.connector.connect(user='dev0', password='Christa1', host='73.158.191.112',
                                      database='inetSpeed')  # 73.158.191.112

        cursor = cnx.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        past = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute(
            "SELECT"
            "  t1.date_time, "
            "  ( SELECT SUM(t2.speed_down) / COUNT(t2.speed_down)"
            "    FROM inetLog AS t2"
            "    WHERE TIMESTAMPDIFF(MINUTE, t1.date_time, t2.date_time) BETWEEN 0 AND 60"
            "  ) AS 'speed_down_ave',"
            "  ( SELECT SUM(t3.speed_up) / COUNT(t3.speed_up)"
            "    FROM inetLog AS t3"
            "    WHERE TIMESTAMPDIFF(MINUTE, t1.date_time, t3.date_time) BETWEEN 0 AND 60"
            "  ) AS 'speed_up_ave'"
            "FROM inetLog AS t1 WHERE t1.date_time BETWEEN %s AND %s"
            "ORDER BY t1.date_time;",
            (past, now))
        # cursor.execute("SELECT datetime, speed_down, speed_up FROM inetLog WHERE datetime BETWEEN %s AND %s;", (past, now))

        downAveData = list()
        upAveData = list()
        for i in cursor:
            downAveData.append((i[0], i[1]))
            upAveData.append((i[0], i[2]))

        line_chart = pygal.DateTimeLine(x_label_rotation=75, truncate_label=-1,
                                        x_value_formatter=lambda dt: dt.strftime('%m-%d %H:%M'))
        line_chart.add("Down Ave Hour", downAveData)
        line_chart.add("Up", upAveData)
        return line_chart.render_response()
    except Exception:
        return(str(Exception))


if __name__ == '__main__':
    app.run(debug=True)
