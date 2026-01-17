#!/usr/bin/env python
# coding: utf-8

from sqlalchemy import create_engine
from tqdm.auto import tqdm
import pandas as pd
import click

@click.command()
@click.option('--sgbd', default='postgresql+psycopg2', help='Database dialect and driver (e.g., postgresql+psycopg2).')
@click.option('--pg_user', default='root', help='Database username.')
@click.option('--pg_pass', prompt=True, hide_input=True, confirmation_prompt=False, help='Database password.')
@click.option('--pg_host', default='localhost', help='Database host.')
@click.option('--pg_port', default='5432', help='Database port.')
@click.option('--pg_db', default='postgres', help='Database name.')
@click.option('--year', default=2021, type=int, help='Year of the dataset.')
@click.option('--month', default=1, type=int, help='Month of the dataset.')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for data ingestion.')
@click.option('--target_table', help='Target table name in the database.')
def run(sgbd, pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize, target_table):
    """
    Ingest NYC Yellow Taxi data into a database.
    """
    engine = create_engine(f'{sgbd}://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # URL for the dataset
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    url = f'{prefix}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz'

    # Data types for parsing
    dtype = {
        "VendorID": "Int32",
        "passenger_count": "Int32",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

    # Columns to parse as dates
    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]

    # Load the data into a DataFrame
    df = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates
    )

    # Iterate over the data in chunks
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    # Print the SQL schema for the DataFrame
    print(pd.io.sql.get_schema(df, name=f'{target_table}_{year}_{month}', con=engine))

    # Create the table and insert data
    print(f'Creating table {target_table}_{year}_{month} in the database...')
    df.head(0).to_sql(name=f'{target_table}_{year}_{month}', con=engine, if_exists='replace')
    print(f'Table {target_table}_{year}_{month} created.')

    print(f'Inserting data into table {target_table}_{year}_{month}...')
    for chunk in tqdm(df_iter):
        chunk.to_sql(name=f'{target_table}_{year}_{month}', con=engine, if_exists='append')

    print(f'Data inserted into table {target_table}_{year}_{month}.')
    print(f'Count of rows inserted: {len(df)}')

if __name__ == '__main__':
    run()