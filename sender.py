import json
import random
import time
import requests
import datetime
from flask import Flask

app = Flask(__name__)
def generate_random_json():


    c1_B2 = {
        "du-id": 1001,
        "measTimeStampRf": f"{datetime.datetime.now()}",
        "nrCellIdentity": 'c1/B2',
        "throughput": random.uniform(1.0, 100.0),
        "x": 0,
        "y": 0,
        "availPrbDl": random.randint(1, 100),
        "availPrbUl": random.randint(1, 100),
        "measPeriodPrb": random.randint(1, 100),
        "pdcpBytesUl": random.randint(1, 100),
        "pdcpBytesDl": random.randint(1, 100),
        "measPeriodPdcpBytes": random.randint(1, 100),
    }
    c1_B13 = {
        "du-id": 1001,
        "measTimeStampRf": f"{datetime.datetime.now()}",
        "nrCellIdentity": 'c1/B13',
        "throughput": random.uniform(1.0, 100.0),
        "x": 0,
        "y": 0,
        "availPrbDl": random.randint(1, 100),
        "availPrbUl": random.randint(1, 100),
        "measPeriodPrb": random.randint(1, 100),
        "pdcpBytesUl": random.randint(1, 100),
        "pdcpBytesDl": random.randint(1, 100),
        "measPeriodPdcpBytes": random.randint(1, 100),
    }
    cell_data = [c1_B2, c1_B13]
    return json.dumps(cell_data)

def send_data_to_receiver():
    while True:
        try:
            json_data = generate_random_json()
            response = requests.post("http://127.0.0.1:5000/receive", json=json.loads(json_data))
            print("Data sent:", json_data, flush=True)  # Set flush=True to force immediate print
            time.sleep(1)
        except Exception as e:
            print("Error:", e, flush=True)  # Print any exceptions that occur
            time.sleep(1)

if __name__ == "__main__":
    print("Sender script started", flush=True)
    send_data_to_receiver()