import pymysql
import pymysql.cursors

conn= pymysql.connect(host='localhost',user='root',password='password',db='trainingplan',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
a=conn.cursor()
add_plan = ("INSERT INTO weeklyhours VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
data_plan = (450, 7.5, 9, 10.5, 12, 6.5, 9.5, 11.5, 12.5, 6.5, 10, 12, 13, 6.5, 11.5, 11.5, 11.5, 6.5, 10.5, 10.5, 10.5, 6.5, 9.5, 7.5, 6.5, 6.5)
a.execute(add_plan, data_plan)
conn.commit()
a.close()
conn.close()
