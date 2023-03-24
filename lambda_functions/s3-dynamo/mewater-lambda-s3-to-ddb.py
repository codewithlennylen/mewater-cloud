import json
import boto3


# AWS SDK config
ddb_client = boto3.client('dynamodb', region_name="us-east-1")
s3_client = boto3.client('s3', region_name="us-east-1")


def lambda_handler(event, context):

    # Get our bucket and file name
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    ddb_item = parse_file(bucket, key)

    dynamo_response = put_record_on_ddb(ddb_item)

    return {
        'statusCode': 200,
        'body': {
            'bucket': bucket,
            'key': key,
            'dynamo_item': ddb_item,
            'dynamo_response_code': dynamo_response['ResponseMetadata']['HTTPStatusCode']
        }
    }


def parse_file(bucket, key) -> dict:

    # Get our object
    response = s3_client.get_object(Bucket=bucket, Key=key)

    # Load object & convert to json
    data = response['Body'].read().decode('utf-8')
    json_doc = json.loads(data)

    # * Leakage Algorithm -> Simple Difference
    leaked_volume = json_doc["inlet_volume"] - \
        (json_doc["outlet1_volume"] + json_doc["outlet2_volume"])

    if leaked_volume > 0:
        print("Leakage Detected")
        # send trigger

    # create item / 'record' for DynamoDB
    ddb_item = {
        "time": str(json_doc["time"]),
        "inlet_volume": str(json_doc["inlet_volume"]),
        "outlet1_volume": str(json_doc["outlet1_volume"]),
        "outlet2_volume": str(json_doc["outlet2_volume"]),
        "leaked_volume": str(leaked_volume)
    }

    return ddb_item


def put_record_on_ddb(ddb_item: dict) -> dict:

    # Specify the table
    response = ddb_client.put_item(
        TableName='mewater-ddb-processed',
        Item={
            "time": {'S': ddb_item["time"]},
            "inlet_volume": {'S': ddb_item["inlet_volume"]},
            "outlet1_volume": {'S': ddb_item["outlet1_volume"]},
            "outlet2_volume": {'S': ddb_item["outlet2_volume"]},
            "leaked_volume": {'S': ddb_item["leaked_volume"]}
        }
    )

    return response
