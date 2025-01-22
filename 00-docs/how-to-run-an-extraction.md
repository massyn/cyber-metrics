# Running a data extraction

## Overview

Each collector is [built](writing-a-collector.md) around the use of environment variables.  A number of variables must be present for the collector to be activated.  The [wrapper](../01-collectors/wrapper.py) process will cycle through all collectors, determine if the environment variables are set, and then initate the extraction.

By using environment variables, you have control over how the extraction process is run.  It can be wrapped into a Docker container, or run standalone using [.env](https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1) files

> Refer to the [collectors](collectors.md) document to see which collectors are supported, and what their required environment variables are.

## Running an extraction

Set your environment variables.  Create an `.env` file, and populate it with the following environment variables.

> These examples assume that you have access to either Crowdstrike Falcon, or TenableIO.  If you don't have those API keys, then this example won't work for you.

```bash
# Crowdstrike Falcon API keys
FALCON_CLIENT_ID="xxx"
FALCON_SECRET="yyy"
# Tenable API Keys
TIO_ACCESS_KEY="xxx"
TIO_SECRET_KEY="yyy"
```

Once the environment variables are set, you can run the extractor.

```bash
$ cd 01-collectors
$ python wrapper.py
```
Upon completion, you will have a `data` folder populated with a number of `json` files.

## Destinations

The collected data can be sent to a number of target destination.  If the environment variable is set, the data will be sent to that target destination.

### Local files

By default the collector will save the collected data to the `../dat/$TAG.json` folder.  Depending on the environment variables defined, you will be able to write the data to other locations too, depending on your particular use case.

| **Environment**            | **Purpose**                                | **Example**            |
|-----------------------------|--------------------------------------------|------------------------|
| `STORE_FILE`       | Specifies the target path on the local disk. | Defaults to `../data/source/$TAG/$TENANCY.json` |

### Postgres

You have the option to save the tables to a Postgres data.  To use Postgres, you need to define the following environment variables.

| **Environment**            | **Purpose**                                | **Example**            |
|-----------------------------|--------------------------------------------|------------------------|
| `STORE_POSTGRES_HOST`       | Specifies the hostname or IP address of the PostgreSQL server. | `localhost` or `db.example.com` |
| `STORE_POSTGRES_USER`       | Defines the username for authenticating with the PostgreSQL database. | `admin_user`           |
| `STORE_POSTGRES_PASSWORD`   | Provides the password for the specified PostgreSQL user.        | `securepassword123`    |
| `STORE_POSTGRES_DBNAME`     | Indicates the name of the PostgreSQL database to connect to.    | `my_database`          |
| `STORE_POSTGRES_PORT`       | Sets the port number for connecting to the PostgreSQL server.   | `5432`                 |
| `STORE_POSTGRES_SCHEMA`     | Specifies the schema within the PostgreSQL database.            | `public`               |

### AWS S3

| **Environment**            | **Purpose**                                | **Example**            |
|-----------------------------|--------------------------------------------|------------------------|
| `STORE_AWS_S3_BUCKET`       | The specific bucket where the data will be stored. | `security-data-collector` |
| `STORE_AWS_S3_KEY`          | The specific key (or filename) to use on S3 | `data/tag=$TAG/year=$YYYY/month=$MM/day=$DD/$UUID.json` |
| `STORE_AWS_S3_BACKUP`       | The specific key (or filename) to use on S3 for the collector backup job | `collector/$TAG/$TENANCY.json` |

### DuckDB

| **Environment**            | **Purpose**                                | **Example**            |
|-----------------------------|--------------------------------------------|------------------------|
| `STORE_DUCKDB`       | Specifies the target path on the local disk. | `../data/database.duckdb` |

## Target path variables

You can customise the path where the target files are to be sent, depending on your particular use case, and how data needs to be ingested.

|**Variable**|**Purpose**|
|--|--|
|`%UUID`|A unique uuid that is created for this specific file.|
|`%TAG`|The data source function|
|`%TENANCY`|The tenancy variable (if defined from an environment variable)|
|`%hh`|Hour|
|`%mm`|Minute|
|`%ss`|Second|
|`%YYYY`|Year|
|`%MM`|Month|
|`%DD`|Day|

### Examples

Store files locally, overwriting it every time when it runs with the latest copy

```bash
export STORE_FILE='../data/source/%TAG/%TENANCY.json'
```

Save the files to an AWS S3 bucket, partition the data by date and uuid to allow ingestion to a tool like Snowflake.

```bash
export STORE_AWS_S3_BUCKET=my-s3-bucket-name
export STORE_AWS_S3_KEY='data/%TAG/%YYYY/%MM/%DD/%UUID.json'
```

## Managing state

When all collectors work fine all the time, there is no issue.  When they fail, and the API is unable to retrieve data, the metrics will not generate.  When running in a Docker-based environment, everytime the docker image spins up, none of the data is available.  Using AWS S3 as a backup storage will allow the last downloaded data to be available for querying by the metric if required.

To utilise the AWS S3 backup mechanism, the following 2 environment variables need to be set.

```bash
export STORE_AWS_S3_BUCKET=my-s3-bucket-name
export STORE_AWS_S3_BACKUP='data/%TAG/%TENANCY.json'
```

## Collector Environment variables

The collector wrapper script utilises the following environment variables.

| **Environment**       | **Purpose**                                | **Default value**                                    |
|-----------------------|--------------------------------------------|------------------------------------------------------|
| `STORE_FILE`          | Defines the local path where the local file will be stored. | `../data/source/%TAG/%TENANCY.json` |
| `STORE_AWS_S3_BACKUP` | Define the AWS S3 bucket where the collector will store its working files. |  `backup/%TAG/%TENANCY.json` |
| `STORE_AWS_S3_KEY` | Similar to the previous parameter.  Use this option if you wanted to write a 2nd AWS file, for example if you wanted to send the data to snowflake, you can use something like `data/tag=%TAG/year=%YYYY/month=%MM/day=%DD/%UUID.json` | |
| `STORE_DUCKDB` | If you are so inclined to send the data to a DuckDB instance, you can specify the DuckDB file path. | |
