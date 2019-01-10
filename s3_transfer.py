from __future__ import print_function
import boto3
import time
import datetime
from decimal import Decimal

ml = boto3.client('machinelearning')


# s3 = boto3.client('s3')
# s3.upload_file('S£_transfer.txt','tutorialsiot','S3_script.txt')

response = ml.predict(
    MLModelId='ml-QQgKl1iHzix',
    Record={
        'DayofWeek' : "Sunday",
        'PreviousDayCalories': str(2060),
        'VeryActiveMin': str(50),
        'SleepMins': str(600)
    },
    PredictEndpoint='https://realtime.machinelearning.us-east-1.amazonaws.com'


)
print(response["Prediction"]["predictedValue"])

title = "Prediction"
number = response["Prediction"]["predictedValue"]
value = Decimal(number)


dynamodb = boto3.resource('dynamodb')
dynamoTable = dynamodb.Table('test_table')
dynamoTable.put_item(

    Item={
        'Name': title,
        'Age' : value

    }
)
