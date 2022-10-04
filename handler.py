from concurrent.futures import process
import json
import boto3
import os

options = {}

if (os.environ["IS_OFFLINE"]):
    options = {
        "region": "localhost",
        "endpoint": "http://localhost:8000"
    }


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def kittens_create(event, context):
    print("Event: ", event)
    print("Context: ", context)
    print("Body: ", event["body"])
    data = json.loads(event["body"])
    print("Data: ", data)
    dynamodb = boto3.client("dynamodb")
    try:
        createResults = dynamodb.put_item(
            TableName=os.environ["DYNAMODB_TABLE_NAME"],
            Item={
                "kittenName": {"S": data["kittenName"]},
                "kittenAge": {"N": str(data["kittenAge"])}
            }
        )
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "message": "Some error occured!"
        }
    print(createResults)
    response = {
        "statusCode": 200,
        "body": json.dumps("Successfully Added Kitten!")
    }
    return response


def kittens_list(event, context):
    print("Event: ", event)
    print("Context: ", context)
    dynamodb = boto3.client("dynamodb")
    getResults = ""
    try:
        getResults = dynamodb.scan(
            TableName=os.environ["DYNAMODB_TABLE_NAME"],
            ProjectionExpression="kittenName, kittenAge"
        )
        # getResults = dynamodb.get_item(
        #     TableName=os.environ["DYNAMODB_TABLE_NAME"],
        #     Key={"kittenName": {"S": "Fluffykins"}}
        # )
    except Exception as e:
        print(e)
        response = {
            "statusCode": 500,
            "body": json.dumps("Some Error Occured!")
        }
        return response
    print("Get Result", getResults)
    response = {
        "statusCode": 200,
        "body": json.dumps(getResults["Items"])
    }
    return response


def kitten_by_name(event, context):
    print("Event: ", event)
    print("Context: ", context)
    print("Name: ", event["pathParameters"]["name"])
    dynamodb = boto3.client("dynamodb")
    getResult = {}
    try:
        getResult = dynamodb.get_item(
            TableName=os.environ["DYNAMODB_TABLE_NAME"],
            Key={"kittenName": {"S": str(event["pathParameters"]["name"])}}
        )
    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps(e.message)
        }
        return response
    print("Get Result: ", getResult)
    response = {
        "statusCode": 200,
        "body": json.dumps(getResult["Item"])
    }
    return response


def kittens_update(event, context):
    pass


def kittens_delete(event, context):
    pass
