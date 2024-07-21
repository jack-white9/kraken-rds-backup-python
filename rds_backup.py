import sys
import boto3
import botocore
import logging
from typing import TypedDict, List
from datetime import datetime, timezone


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# define custom snapshot type
class Snapshot(TypedDict):
    IsSnapshotSuccessful: bool
    DBClusterSnapshotIdentifier: str
    DBClusterIdentifier: str
    DBClusterSnapshotArn: str
    SnapshotType: str
    SnapshotCreateTime: str


def create_snapshot(db: str) -> Snapshot:
    client = boto3.client("rds")
    utc_timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    snapshot_id = f"{db}-snapshot-{utc_timestamp}"
    try:
        response = client.create_db_cluster_snapshot(
            DBClusterSnapshotIdentifier=snapshot_id,
            DBClusterIdentifier=db,
            Tags=[{"Key": "Database", "Value": db}],
        )
        logger.info(f"Snapshot created: {snapshot_id}")
        data = response["DBClusterSnapshot"]
        return {
            "IsSnapshotSuccessful": True,
            "DBClusterSnapshotIdentifier": snapshot_id,
            "DBClusterIdentifier": db,
            "DBClusterSnapshotArn": data["DBClusterSnapshotArn"],
            "SnapshotType": data["SnapshotType"],
            "SnapshotCreateTime": data["SnapshotCreateTime"].strftime("%Y%m%d%H%M%S"),
        }
    except botocore.exceptions.ClientError as error:
        logger.error(f"Error creating snapshot for {db}: {error}")
        return {
            "IsSnapshotSuccessful": False,
            "DBClusterSnapshotIdentifier": snapshot_id,
            "DBClusterIdentifier": db,
            "DBClusterSnapshotArn": None,
            "SnapshotType": None,
            "SnapshotCreateTime": None,
        }
    except botocore.exceptions.ParamValidationError as error:
        raise ValueError(f"The provided parameters are incorrect: {error}")
    except Exception as error:
        raise Exception(f"Error creating snapshot for {db}: {error}")


def create_db_backups(dbs: List[str]) -> List[Snapshot]:
    backups = []
    for db in dbs:
        backup = create_snapshot(db)
        backups.append(backup)
    return backups


if __name__ == "__main__":
    # command line execution
    if len(sys.argv) < 2:
        print("Usage: python rds_backup.py <db-1> <db-2> <db-2> ...", file=sys.stderr)
    dbs = sys.argv[1:]
    backups = create_db_backups(dbs)
else:
    # export create_db_backups to other files
    __all__ = ["create_db_backups"]
