import flask
from flask import request, Response 
import json

from traceback import format_exc

from lambda_handler import lambda_handler

app = flask.Flask(__name__)
app.config["DEBUG"] = True

from flask_cors import CORS
CORS(app)

def dict_to_json(target_dict):
    return json.dumps(target_dict)

#for getting the full traceback of an exception:
def get_traceback():
    return format_exc()

#used for error message when the , to emulate API gateway
def formatFailResponse(message,status,content_type="application/json"):
    response = Response(
        response = dict_to_json({"success": 0, "description": message}),
        status = status,
        headers = {"Content-Type": content_type}
    )
    return response

#used for successful message when the lambda_handler execution is successful 
def formatSuccessResponse(result,status,content_type="application/json"):
    response = Response(
        response = result,
        status = status,
        headers = {"Content-Type": content_type}
    )
    return response

@app.route('/<category>/<action>', methods=['POST'])
def server(category,action):
    #blocking request with wrong error type
    json_type = 'application/json'
    form_type = 'multipart/form-data'
    url_form_type = 'application/x-www-form-urlencoded'
    #print(request.get_data())
    #parseForm(request.get_data(),request.content_type)
    #form_type = 

   
  
    

    #mocking the aws_lambda message input
    event = {}

    #if empty data, do not provide the body to the lambda_handler, this mimicks the behavior of the HTTP API Gateway
    if not (request.get_data() == b""):
        if request.content_type == url_form_type or form_type in request.content_type: #if content type is one of these two, encode it as base64 to mimic aws behavior
            event["body"] = bytes_to_base64string(request.get_data()) 
            event["isBase64Encoded"] = True
        else:
            event["body"] = request.get_data(as_text=True)
            event["isBase64Encoded"] = False
            


    event["pathParameters"] = {}
    event["headers"] = {}
    event["pathParameters"]["category"] = category
    event["pathParameters"]["action"] = action
    #if these following headers are not provided, do not pass it to the lambda handler
    if not(request.content_type == None):
        event["headers"]["content-type"] = request.content_type
    if not(request.remote_addr == None):
        event["headers"]["x-forwarded-for"] = request.remote_addr
    
    
    try:
        result = lambda_handler(event,None)
    except Exception as e:
        #print the whole excption traceback 
        print(get_traceback())
        #if this response is triggered, this means the exception handling within the handler is not completely valid
        #in the aws setup, response will be 500 {"message":"Internal Server Error"}
        return formatFailResponse(get_traceback(), 555)

    #converting back to dict to get the result and status code
    
    return formatSuccessResponse(result["body"],result["statusCode"])

app.run()