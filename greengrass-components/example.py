import os
import sys
import time
import csv
import json 

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
sys.path.append(file_dir + "/dependencies")

message = "Hello, %s!" % sys.argv[1]
message += " Greetings from your first Greengrass component."

# Print the message to stdout, which Greengrass saves in a log file.
print(message)

# from awsiot import greengrasscoreipc

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    QOS,
    PublishToIoTCoreRequest
)

TIMEOUT = 10
print("connecting")
ipc_client = awsiot.greengrasscoreipc.connect()

print("connecting great!")

topic = "amboo/pump-test"
# message = "Hello, World from greengrass"
qos = QOS.AT_LEAST_ONCE

data_file = file_dir + "/sensor_test.csv"
with open(data_file, newline='') as f:
    reader = csv.DictReader(f) 
    for row in reader:
        c_utc_time = time.strftime("%Y%m%d%H%M%S", time.gmtime()) 

        t = {"Timestamp": c_utc_time}
        t.update(row)

        j = json.dumps(t)
        # print(j)  

        request = PublishToIoTCoreRequest()
        request.topic_name = topic
        request.payload = bytes(j, "utf-8")
        request.qos = qos
        operation = ipc_client.new_publish_to_iot_core()
        operation.activate(request)
        future = operation.get_response()
        future.result(TIMEOUT)   

        time.sleep(5)          

print("Done for the publish")
