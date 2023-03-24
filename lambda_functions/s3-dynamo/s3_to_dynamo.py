import os
import json
import boto3
from dotenv import load_dotenv


# Environment Variables
# ? We'll use AWS Secrets in prod.
load_dotenv()
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# AWS SDK config
ddb_client = boto3.client('dynamodb', region_name="us-east-1",
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


# Dynamodb Partition Key -> time(string)
# time
# inlet_volume
# outlet_volume1
# outlet_volume2
# leakage

# TODO: Get files from s3
def parse_file():
    path = 's3-data/_1673783312034'

    with open(path, 'r') as file:
        doc = file.readline()
        json_doc = json.loads(doc)

    # * Leakage Algorithm -> Simple Difference
    leaked_volume = json_doc["inlet_volume"] - \
        (json_doc["outlet1_volume"] + json_doc["outlet2_volume"])

    # TODO: Trigger valve_shutdown_lambda
    # TODO: Send Alert SMS
    # TODO: Send Alert Email
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


def put_record_on_ddb():
    ddb_item = parse_file()
    print(ddb_item)

    # Specify the table
    response = ddb_client.put_item(
        TableName='mewater-ddb-processed',
        # Item={
        #     'time': ddb_item["time"],
        #     'info': ddb_item
        # }
        # Item={
        #     "time": ddb_item["time"],
        #     "inlet_volume": ddb_item["inlet_volume"],
        #     "outlet1_volume": ddb_item["outlet1_volume"],
        #     "outlet2_volume": ddb_item["outlet2_volume"],
        #     "leaked_volume": ddb_item["leaked_volume"]
        # }

        # https://www.section.io/engineering-education/getting-started-with-aws-dynamodb/
        Item={
            "time": {'S': ddb_item["time"]},
            "inlet_volume": {'S': ddb_item["inlet_volume"]},
            "outlet1_volume": {'S': ddb_item["outlet1_volume"]},
            "outlet2_volume": {'S': ddb_item["outlet2_volume"]},
            "leaked_volume": {'S': ddb_item["leaked_volume"]}
        }
    )

    print(response)
    return response


# parse_file()
put_record_on_ddb()
