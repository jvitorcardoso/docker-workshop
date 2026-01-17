#!/bin/bash

docker run -it --rm \
    --network=pg-network \
    taxi_ingest:v01 \
        --pg_user=root \
        --pg_pass=root \
        --pg_host=pgdatabase \
        --pg_port=5432 \
        --pg_db=ny_taxi \
        --year=2021 \
        --month=3 \
        --target_table=yellow_taxi_data \
        --chunksize=100000