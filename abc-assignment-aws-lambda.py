import json
import time
import csv
import os
import socket   
import boto3
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def printDeviceInfo():
    # Python Program to Get IP Address
    hostname = socket.gethostname()   
    IPAddr = socket.gethostbyname(hostname)   
    print("Your Computer Name is:" + hostname)   
    print("Your Computer IP Address is:" + IPAddr)   

def check_ping(hostname):
    #hostname = "taylor"
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"
    print(pingstatus)
    return pingstatus

def lambda_handler(event, context):
    print("this is the pump data converter")
    print(event)
    #printDeviceInfo()

    ep_name = 'abc-pump-anomaly-sagemaker'
    sm_rt = boto3.Session().client('runtime.sagemaker')

    org = "abc"
    bucket = "abc"
    db_url = os.getenv('INFLUXDB_URL')
    db_token = os.getenv('INFLUXDB_TOKEN')
    print(db_url)
    
    #check_ping(db_host)
    
    client = InfluxDBClient(url=db_url, token=db_token)
    write_api = client.write_api(write_options=SYNCHRONOUS)  

    # input shall be csv format
    t = event
    t.pop("Timestamp")
    
    # compose the input for inference
    input = ",".join(t.values()) 
    print(input)
    
    # send sensor data to influxdb
    for x in t:
    #print(t[x])
    #print(type(t[x]))
        tmp = 0.0
        if (t[x]):
            tmp = float(t[x])  
        t[x] = tmp    

    data_sensor = {
        "measurement": "sensor",
        "tags": {"asset": "pump1"},
        "fields": t
    }
    write_api.write(bucket, org, data_sensor) 
    print("success write sensor data to influxdb")

    response = sm_rt.invoke_endpoint(EndpointName=ep_name, 
                                        ContentType='text/csv',       
                                        Accept='text/csv', Body=input)

    response = response['Body'].read().decode("utf-8")
    print ("inference result:" + response)
    
    #send inference result to influxdb
    print(response)
    status = 0
    label = response[:1]

    if label == "B":
        status = 2
    elif label == "R":
        status = 1

    data_inference = {
        "measurement": "machine_status",
        "tags": {"asset": "pump1"},
        "fields": {"status": status}
    }
    print(data_inference)
    write_api.write(bucket, org, data_inference)
