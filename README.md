# RDS Backup

This script performs an RDS backup by creating database snapshots on a list of provided Amazon Aurora clusters. The backup is performed by the `create_db_backups` function.

## Snapshot Data Structure

A custom `Snapshot` class has been defined to contain the snapshot data structure. A list of `Snapshot` values will be returned by the `create_db_backups` function.

```py
class Snapshot(TypedDict):
    IsSnapshotSuccessful: bool
    DBClusterSnapshotIdentifier: str
    DBClusterIdentifier: str
    DBClusterSnapshotArn: str
    SnapshotType: str
    SnapshotCreateTime: str
```

## Unit Testing

Unit tests are performed using Pytest as the test runner and Moto to mock AWS services. Tests can be viewed in [test_rds_backup.py](./test_rds_backup.py).

Run unit tests using the following command:

```sh
pytest
```

## Installation

### Manual Installation

1. Setup virtual environment. _**Note**: Although Python 3.8 has been used for this example, the script is forward-compatible with versions >= 3.8. Use your preferred version._

```sh
python3.8 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies

```sh
pip install -r requirements.txt
```

### Docker Image

1. Build Docker image called `rds_backup`.

```sh
docker build -t rds_backup .
```

## Usage

### Command Line Usage (Manual)

Invoke the `rds_backup.py` script with a space-separated list of strings.

```sh
python rds_backup.py db-1 db-2 db-3
```

### Command Line Usage (Docker)

Run the `rds_backup` Docker image from [Docker Installation](#docker-installation), passing `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_DEFAULT_REGION` as required.

```sh
docker run \
  -e AWS_ACCESS_KEY_ID=<aws_access_key_id> \
  -e AWS_SECRET_ACCESS_KEY=<aws_secret_access_key> \
  -e AWS_DEFAULT_REGION=<aws_default_region> \
  rds_backup db-1 db-2 db-3
```

### Import Usage

Import `create_db_backups` from `rds_backup` and provide the function a list of strings.

```py
from rds_backup import create_db_backups

create_db_backups(["db-1", "db-2", "db-3"])
```
