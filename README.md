# AWS_Serverless_Walkthrough  
- This repo would mainly include build a serverless environment with aws lambda and aws fargate. 
- Purpose : lower the cost  
- This demo would be setting up an API to store some random data in MySQL DB (aws RDS)
```
- Flow :  | Client enter url  
                    |── Call ──> aws API Gateway  
                                 |── Trigger ──> aws lambda 
                                                 |── Insert random data --> DB  
                                                 |── Trigger --> aws fargate  
                                                                 |── Insert random data --> DB  
```

## Fargate

## Lambda 
Credit : BWong951
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
Remarks: There is limit on upload file size 10MB . If greater , push it to aws s3 first then link url.  
