#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table = params.table
    url = params.url

    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url}' -O {csv_name}")

    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv('green_tripdata_2019-10.csv.gz', compression='gzip',iterator=True, chunksize=100000)

    df = next(df_iter)

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists='replace')

    df.to_sql(name='green_taxi_data', con=engine, if_exists='append')


    while True:
        t_start=time()
        
        df = next(df_iter)
        
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

        df.to_sql(name='green_taxi_data', con=engine, if_exists='append')

        t_end=time()

        print('inserted another chunk...., took %.3f seconds' %(t_end-t_start))

    df_zone = pd.read_csv('taxi_zone_lookup.csv')

    df_zone.dtypes

    df_zone.head(n=0).to_sql(name='taxi_zone_lookup', con=engine, if_exists='replace')

    df_zone.to_sql(name='taxi_zone_lookup', con=engine, if_exists='append')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                        description='Ingest CSV data to Postgres',
                        )
    #user, password, host, port, database name, table name, url of the CSV

    parser.add_argument('--user', help='username for Postgres')
    parser.add_argument('--password', help='password for Postgres')
    parser.add_argument('--host', help='host of Postgres')
    parser.add_argument('--port', help='port of Postgres')
    parser.add_argument('--db', help='Postgres database name')
    parser.add_argument('--table', help='Postgres table name where we will write the results to')
    parser.add_argument('--url', help='url of the CSV file')

    args = parser.parse_args()
    main(args)






