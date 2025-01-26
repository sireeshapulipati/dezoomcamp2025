# dezoomcamp2025

## Module 1: Docker-Terraform Homework

Q1:

```
docker run -it --entrypoint bash python:3.12.8

```

```
pip --version

```

Q2: Postgres setup

```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v /Users/sireesha/dezoomcamp2025/01-docker-terraform/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
  
```

Install pgcli:
  ```
  pip install pgcli
 
  ```

Connect to postgres database:
  ```
  sudo pgcli -h localhost -p 5432 -U root -d ny_taxi
  
  ```

Install PgAdmin:
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4

```

Create network to connect posgres AND PgAdmin containers:
```
docker network create pg-network

```

Now restart postgres and pgadmin containers with this network specification

```
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v /Users/sireesha/dezoomcamp2025/01-docker-terraform/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name=pg-database \
  postgres:13

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name=pg-admin-nw \
  dpage/pgadmin4

```

Build Docker image and run it
```
URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"

docker build -t taxi_ingest:v001

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table=green_taxi_trips \
    --url=${URL}