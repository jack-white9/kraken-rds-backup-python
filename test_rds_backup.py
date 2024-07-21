import boto3
import pytest
from moto import mock_aws
from rds_backup import create_snapshot, create_db_backups


RDS_CLUSTER_IDENTIFIER = "test-db-cluster"


@pytest.fixture
def mock_rds_cluster():
    with mock_aws():
        client = boto3.client("rds")
        client.create_db_cluster(
            DBClusterIdentifier=RDS_CLUSTER_IDENTIFIER,
            Engine="aurora-postgresql",
            MasterUsername="foo",
            MasterUserPassword="foobar12",
        )
        yield client


def test_create_snapshot_success(mock_rds_cluster):
    snapshot = create_snapshot(RDS_CLUSTER_IDENTIFIER)
    assert snapshot["IsSnapshotSuccessful"] == True
    assert snapshot["DBClusterSnapshotIdentifier"].startswith(RDS_CLUSTER_IDENTIFIER)
    assert snapshot["DBClusterIdentifier"] == RDS_CLUSTER_IDENTIFIER
    assert snapshot["DBClusterSnapshotArn"] is not None
    assert snapshot["SnapshotType"] == "manual"
    assert snapshot["SnapshotCreateTime"] is not None


def test_create_snapshot_failure(mock_rds_cluster):
    snapshot = create_snapshot("non-existent-cluster")
    assert snapshot["IsSnapshotSuccessful"] == False
    assert snapshot["DBClusterSnapshotIdentifier"].startswith("non-existent-cluster")
    assert snapshot["DBClusterIdentifier"] == "non-existent-cluster"
    assert snapshot["DBClusterSnapshotArn"] is None
    assert snapshot["SnapshotType"] is None
    assert snapshot["SnapshotCreateTime"] is None


def test_create_db_backups_success(mock_rds_cluster):
    dbs = [RDS_CLUSTER_IDENTIFIER]
    backups = create_db_backups(dbs)
    backup = backups[0]

    assert len(backups) == 1
    assert backup["DBClusterSnapshotIdentifier"].startswith(RDS_CLUSTER_IDENTIFIER)
    assert backup["DBClusterIdentifier"] == RDS_CLUSTER_IDENTIFIER
    assert backup["DBClusterSnapshotArn"] is not None
    assert backup["SnapshotType"] == "manual"
    assert backup["SnapshotCreateTime"] is not None


def test_create_db_backups_failure(mock_rds_cluster):
    dbs = ["non-existent-cluster"]
    backups = create_db_backups(dbs)
    backup = backups[0]

    assert len(backups) == 1
    assert backup["IsSnapshotSuccessful"] == False
    assert backup["DBClusterSnapshotIdentifier"].startswith("non-existent-cluster")
    assert backup["DBClusterIdentifier"] == "non-existent-cluster"
    assert backup["DBClusterSnapshotArn"] is None
    assert backup["SnapshotType"] is None
    assert backup["SnapshotCreateTime"] is None
