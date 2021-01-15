import pymysql 
import random

import rds_config

x=random.randint(1,100)
try:    
    conn = pymysql.connect(host=rds_config.rds_host,port=3306,user=rds_config.username,password=rds_config.password,db=rds_config.db_name,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cur:
        sql="""INSERT INTO dt_history (entity,dataset) VALUES ({},"briangay") """.format(x)
        cur.execute(sql)
        conn.commit()
    conn.close()
except Exception as e:
    print("Failed")
    raise e
