import json
import boto3
import os


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
    dynamodb = boto3.client("dynamodb")
    try:
        createResults = dynamodb.put_item(
            TableName=os.environ["DYNAMODB_TABLE_NAME"],
            Item={
                "kittenName": {"S": "Tom"},
                "kittenAge": {"N": "20"}
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
        return {
            "statusCode": 500,
            "message": "Some error occured!"
        }
    print("Get Result", getResults)
    response = {
        "statusCode": 200,
        "body": json.dumps(getResults["Items"])
    }
    return response


def kittens_update(event, context):
    pass


def kittens_delete(event, context):
    pass
