# AWS_Serverless_Walkthrough  
- This repo would mainly include build a serverless environment with aws lambda and aws fargate. 
- Purpose : lower the cost  
- This demo would be setting up an API to store some random data in MySQL DB 
```
- Flow :  .  
          | Client enter url  
          |── Call ──> aws API Gateway  
                       |── Trigger ──> aws lambda 
                                       |── Insert random data --> DB  
                                       |── Trigger --> aws fargate  
                                                       |── Insert random data --> DB  
```

## Fargate

## Lambda [Cr]
1. Creating a Lambda function to handle the request passed by API Gateway




