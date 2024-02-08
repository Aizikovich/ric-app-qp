# ==================================================================================
#  Copyright (c) 2020 HCL Technologies Limited.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ==================================================================================

"""
This Module is temporary for pushing data into influxdb before dpeloyment of QP xApp. It will depreciated in future, when data will be coming through KPIMON
"""

import datetime
import time
import pandas as pd
from src.database import DATABASE
from configparser import ConfigParser
from flask import Flask, request

app = Flask(__name__)

class INSERTDATA(DATABASE):

    def __init__(self):
        super().__init__()
        self.connect()

    def createdb(self, dbname):
        print("Create database: " + dbname)
        self.client.create_database(dbname)
        self.client.switch_database(dbname)

    def dropdb(self, dbname):
        print("DROP database: " + dbname)
        self.client.drop_database(dbname)

    def dropmeas(self, measname):
        print("DROP MEASUREMENT: " + measname)
        self.client.query('DROP MEASUREMENT '+measname)

    # def assign_timestamp(self, df):
    #     steps = df['measTimeStampRf'].unique()
    #     for timestamp in steps:
    #         d = df[df['measTimeStampRf'] == timestamp]
    #         d.index = pd.date_range(start=datetime.datetime.now(), freq='1ms', periods=len(d))
    #         self.client.write_points(d, self.cellmeas)
    #         time.sleep(0.4)
    def assign_timestamp(self, data):
        df = pd.DataFrame(data)
        # Do something with the data here
        time.sleep(1)  # Simulate a delay
        steps = df['measTimeStampRf'].unique()
        for timestamp in steps:
            d = df[df['measTimeStampRf'] == timestamp]
            d.index = pd.date_range(start=datetime.datetime.now(), freq='1ms', periods=len(d))
            self.client.write_points(d, self.cellmeas)
            time.sleep(0.4)


def populatedb():
    # inintiate connection and create database UEDATA
    db = INSERTDATA()
    df = pd.read_csv('src/cells.csv')
    print("Writin data into influxDB")
    while True:
        db.assign_timestamp(df)

@app.route('/receive', methods=['POST'])
def receive():

    try:
        received_data = request.json
        print("Received data:", pd.DataFrame(received_data), flush=True)
        if received_data is not None:
            db.assign_timestamp(received_data)
            received_data = None
        else:
            db.assign_timestamp("No data received")
            time.sleep(1)
        return "Data received successfully!"

    except Exception as e:
        print("Error:", e, flush=True)
        return "Error occurred while receiving data"


if __name__ == "__main__":
    db = INSERTDATA()
    app.run(port=5000)
