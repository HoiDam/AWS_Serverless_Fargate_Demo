

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