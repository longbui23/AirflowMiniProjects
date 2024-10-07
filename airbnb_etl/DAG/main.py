from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_go

import pandas as pd
import sqlite3
import os

dag_path = os.getcswd()

def transform_data():
    booking = pd.read_csv(f"{dag_path}/Data/booking.csv")
    client = pd.read_csv(f"{dag_path}/raw_data/client.csv")
    hotel = pd.read_csv(f"{dag_path}/raw_data/hotel.csv")

    #merging
    data = pd.merge(booking, client, on="client_id")
    data.rename(columns={"name":"client_name","type":"client_type"},inplace=True)

    data = pd.merge(data,hotel,on='hotel_id')
    data.rename(columns={'name':'hotel_name'},inplace=True)

    #datetime format consistency
    data.booking_date = pd.to_datetime(data.booking_date, infer_datetime_format=True)

    #convert currency
    data.loc[data.currency == 'EUR', ['booking_cost']] = data.booking_cost * 0.8
    data.currency.replace("EUR", "GBP", inplace=True)

    #remove colunms
    data = data.drop('address',1)

    #load data
    data.to_csv(f"{dag_path}/processessed_data.csv",index=False)

def load_data():
    conn = sqlite3.connect(("/usr/local/airflow/db/airbnb.db"))
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS booking_record (
                    client_id INTEGER NOT NULL,
                    booking_date TEXT NOT NULL,
                    room_type TEXT(512) NOT NULL,
                    hotel_id INTEGER NOT NULL,
                    booking_cost NUMERIC,
                    currency TEXT,
                    age INTEGER,
                    client_name TEXT(512),
                    client_type TEXT(512),
                    hotel_name TEXT(512),
              );
              ''')
    
    records = pd.read_csv(f"{dag_path}/processed_data/processed_data.csv")
    records.to_sql('booking_record',conn,if_exists='replace',index=False)


# initializing the default arguments that we'll pass to our DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(5)
}

ingestion_dag = DAG(
    'booking_ingestion',
    default_args=default_args,
    description='Aggregates booking records for data analysis',
    schedule_interval=timedelta(days=1),
    catchup=False
)

task_1 = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=ingestion_dag,
)

task_2 = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=ingestion_dag,
)


task_1 >> task_2