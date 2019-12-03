import datetime
import mysql.connector
import speedtest


curr_min = datetime.datetime.now().strftime("%M")

if (int(curr_min) % 15 == 0):
#if (0==0):
    cnx = mysql.connector.connect(user='dev0', password='Christa1',
                                  host='127.0.0.1',
                                  database='inetSpeed')
    cursor = cnx.cursor()
    servers = []
    threads = None

    st = speedtest.Speedtest()
    st.get_servers(servers)
    st.get_best_server()
    
    downLst = list()
    upLst = list()
    
    startTime = datetime.datetime.now()
    for x in range(0, 3):
        downLst.append( st.download(threads=threads) / 1000000)
        upLst.append( st.upload(threads=threads) / 1000000)
        datetime.time.sleep(1)
    endTime = datetime.datetime.now()

    down = (downLst[0] + downLst[1] + downLst[2]) / 3
    up = (upLst[0] + upLst[1] + upLst[2]) / 3
    
    timeDiff = (endTime - startTime) / 2
    aveTime = startTime + timeDiff
    dt = aveTime.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("INSERT INTO inetLog(datetime, speed_down, speed_up) "
                   "VALUES (%s, %s, %s)", (dt, down, up))
    cnx.commit()

    cursor.close()
    cnx.close()

