# AWS_Serverless_Walkthrough  
- This repo would mainly include building a serverless environment with aws lambda and aws fargate. 
- Purpose : lower the cost  
- This demo would be setting up an API to store some random data in aws RDS (MySQL)
- Flow :  
```
| Client enter url  
        |── Call ──> aws API Gateway  
                     |── Trigger ──> aws lambda 
                                     |── Insert random data --> DB  
                                     |── Trigger --> aws fargate  
                                                     |── Insert random data --> DB  
```
---
## Fargate
### 1. Prepare docker container 
- Package the code with docker framework   
- Two choices to push container to public
  1. Dockerhub 
  ref: [HoiDam/PythonIPYNB_Playground](https://github.com/HoiDam/PythonIPYNB_Playground#guide-docker-environment-required-)
  2. AWS ECR
  No ref here . Not yet tried
### 2. Create Task Definitions
- Task Definitions would store your pull your container file every task get triggered
Setup procedure:
1. Enter the front page of AWS ECS 
2. Go to Task Definitions
3. Create new Task Defintion
4. Choose Fargate
5. Type your task definition name
6. Go to Container Defintions and click "Add container"
7. Click Create
### 3. Create Clusters
- Clusters would be an area to store all your tasks run and save the logs
Setup procedure:
1. Go to Clusters
2. Click "Networking only" and "next step"
3. Type your cluster name 
4. Click create
### 4. Generate keys 
- Get the aws access keys for the program to run
- Need certain permissions
Setup procedure:
1. Go to AWS IAM
2. Go to Users
3. Click "Add user"
4. Enter Username
5. Choose access type : Programmatic access
6. Choose attach exisiting policies directly and choose belows policy
> AmazonECS_FullAccess
7. Skip all next and Click Create user
8. Click the user that you created
9. Go to security credentials
10. Create access key
11. Copy the keys to your secret file (DO NOT EXPOSE IT)
### 5. Prepare the code to trigger the created task
- using boto3/pymysql library  
- create client connection  
```
client=boto3.client("ecs",  
                aws_access_key_id=key,   
                aws_secret_access_key=pw,   
                region_name="ap-east-1"  
                )
```  
Access + Secret keys = The keys which saved in secret file  
Region name = Current AWS Region code (E.g ap-east-1) 
```
response = client.run_task(
        cluster='fargatetest', # name of the cluster
        launchType = 'FARGATE',
        taskDefinition='fargatetest:1', # replace with your task definition name and revision
        count = 1,
        platformVersion='LATEST',
        networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [
                        'subnet-123456', # replace with your public subnet or a private with NAT
                        'subnet-233456' # Second is optional, but good idea to have two
                    ],
                    'securityGroups':[
                        'sg-123456'
                    ],
                    'assignPublicIp': 'ENABLED', # dockerhub container : enabled ; aws ECR : disabled 
                }
            }   
    )
```
cluster = The cluster name you created  
taskDefinition = The task definition name you created  
vpcConfiguration = same subnets with aws RDS 

---
## Lambda 
Credit : [Bwong951](https://github.com/Brian951)
### 1. Prepare code with aws lambda environemnt
`server.py` is an aws lambda written for local testing  
`python server.py` to test your code written in `lambda_handler.py`

### 2. Creating a Lambda function to handle the request passed by API Gateway
Setup procedure:
1. Enter the front page of AWS Lambda
2. Click on "Create Function"
3. Select "Author from scratch", type a function name and select "Python 3.7" for "Runtime". Then click "Create Function"
4. Click "Edit" on the "Basic settings" panel.
5. Type "lambda_handler.handler" under the "Handler" field
6. Click "Save"

### 3. Connect RDS (MySQL DB)
#### Best practice: Same VPC & Security Group for lambda & rds
Setup procedure:
1. Enter the front page of your Lambda function
2. Select the same VPC as your database instance under the "VPC" field
3. Select the same subnets under as your database under the "Subnets" field
4. Select the same security group as  your database under the "Security groups" field  
(note that if your security group does not allow inbound connection from your security group, you cannot assess the API)
5. Under the VPC panel, navigate to the "Security Groups" page and click on the security group used by the target RDS.
6. Under "Inbound Rules", click "Edit Inbound Rules".
7. Add a rule with "MYSQL/Aurora" (or "All Traffic", I have not tested with "MYSQL/Aurora" yet) as "Type",  
and set "Source" as "Custom" and set the value as the Security Group ID of the current secutiry group (e.g. sg-xxxxxx). 
#### Another way: Allow the IP of the NAT Gateway to connect to the RDS
Setup procedure:
1. Under the VPC panel, navigate to the "Security Groups" page and click on the security group used by the target RDS.
2. Under "Inbound Rules", click "Edit Inbound Rules".
3. Add a rule with "MYSQL/Aurora" as "Type", and set "Source" as "Custom" and set the value as the Elastic IP of that NAT Gateway.
4. Click "Save rules".

### 4. Lambda Role Permission Setup
Setup procedure:
1. Enter the front page of your Lambda function
2. Click "Edit" on the "Basic settings" panel
3. Click on the blue text "View the <role name> role" to enter the summary page of this role
4. Attach policies to the role
> ec2:CreateNetworkInterface  
> ec2:DescribeNetworkInterfaces  
> ec2:DeleteNetworkInterface (optional)             
          
### 5. API Gateway Setup
Setup procedure (HTTP API):
1. Create an HTTP API under the API Gateway console, select the lambda function for this project as the integration.
2. Configure the default route mthod as POST.
3. Set the resource path as /{category}/{action}          
4. Go to the CORS panel of your API.
5. Click "Edit".
6. Type "*" under Access-Control-Allow-Origin and click "Add".
7. Type "*" under Access-Control-Allow-Headers and click "Add".
8. Pick POST and GET under "Access-Control-Allow-Methods".
9. Click "Save".          
          
### 6. Upload the codes to lambda
As lambda do not provide a server to install packages . Upload the codes with libraries file is needed .  
- Remarks:  
> There is limit on upload file size 10MB . If greater , push it to aws s3 first then link url.  
