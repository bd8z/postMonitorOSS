import base64
import datetime
import json
import uuid

import boto3

s3 = boto3.client('s3')
    

def lambda_handler(event, context):
    try:
        fileExtension = event["extension"]
        fileName = str(uuid.uuid4()) + "." + fileExtension
        path_w = "/tmp/" + fileName
        
        wbData = base64.b64decode(event["file"])
        
        f = open(path_w, 'wb')
        f.write(wbData)
        f.close()
        s3.upload_file(path_w, '***', 'NewImage.jpg')
        
        # TODO implement
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('bad request!')
        }