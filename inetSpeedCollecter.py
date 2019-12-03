import datetime
import mysql.connector
import speedtest

curr_min = datetime.datetime.now().strftime("%M")

if (int(curr_min) % 3 == 0):
#if (0==0):
    cnx = mysql.connector.connect(user='dev0', password='Christa1',
                                  host='73.158.191.112',
                                  database='inetSpeed')
    cursor = cnx.cursor()
    servers = []
    threads = None

    st = speedtest.Speedtest()
    st.get_servers(servers)
    st.get_best_server()

    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    down = (st.download(threads=threads) / 1000000)
    up = (st.upload(threads=threads) / 1000000)

    cursor.execute("INSERT INTO inetLog(datetime, speed_down, speed_up) "
                   "VALUES (%s, %s, %s)", (dt, down, up))
    cnx.commit()

    cursor.close()
    cnx.close()
