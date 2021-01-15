import pymysql
import random
import json

import boto3
from secret import key , pw

import rds_config

def triggerFargate():
    client=boto3.client("ecs",
                aws_access_key_id=key, 
                aws_secret_access_key=pw, 
                region_name="ap-east-1"
                )

    response = client.run_task(
        cluster='fargatetest', # name of the cluster
        launchType = 'FARGATE',
        taskDefinition='fargatetest:1', # replace with your task definition name and revision
        count = 1,
        platformVersion='LATEST',
        networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [
                        'subnet-0a4883972779b39f0', # replace with your public subnet or a private with NAT
                        'subnet-0859ee113a1cb9e21' # Second is optional, but good idea to have two
                    ],
                    'securityGroups':[
                        'sg-03dd8dbd6fae4a8ed'
                    ],
                    'assignPublicIp': 'ENABLED',
                }
            }   
    )

    print(str(response))

def insertion():
    x=random.randint(101,200)
    try:    
        conn = pymysql.connect(host=rds_config.rds_host,port=3306,user=rds_config.username,password=rds_config.password,db=rds_config.db_name,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
        with conn.cursor() as cur:
            sql="""INSERT INTO dt_history (entity,dataset) VALUES ({},"homobrian951-lambda") """.format(x)
            cur.execute(sql)
            conn.commit()
        conn.close()
        return "Done"
    except Exception as e:
        raise e
        return "Failed"

    triggerFargate()

def lambda_handler(event, context):
    # TODO implement
    val=insertion()    
        
    return {
        'statusCode': 200,
        'body': json.dumps(val)
    }

