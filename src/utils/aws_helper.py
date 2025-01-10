import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def test_aws_connection(profile_name=None):
    """
    Test the connection to AWS using the provided profile.
    Args:
        profile_name (str): AWS profile name (optional).
    Returns:
        dict: Details about the caller identity if successful.
    Raises:
        Exception: If the connection test fails.
    """
    try:
        session = boto3.Session(profile_name=profile_name)
        client = session.client("sts")
        response = client.get_caller_identity()
        return {
            "Account": response["Account"],
            "UserId": response["UserId"],
            "Arn": response["Arn"],
        }
    except (NoCredentialsError, PartialCredentialsError):
        raise Exception("AWS credentials are missing or incomplete.")
    except Exception as e:
        raise Exception(f"Failed to connect to AWS: {e}")


def fetch_dashboard_metrics(profile_name=None):
    """
    Fetch metrics for the Nova dashboard.
    Args:
        profile_name (str): AWS profile name (optional).
    Returns:
        dict: Dictionary containing dashboard metrics.
    """
    try:
        session = boto3.Session(profile_name=profile_name)
        rds_client = session.client("rds")
        backup_client = session.client("backup")

        snapshots = rds_client.describe_db_snapshots()["DBSnapshots"]
        total_snapshots = len(snapshots)
        total_size_gb = sum(snapshot["AllocatedStorage"] for snapshot in snapshots)

        vaults = backup_client.list_backup_vaults()["BackupVaultList"]
        total_vaults = len(vaults)

        jobs = backup_client.list_backup_jobs()["BackupJobs"]
        successful_jobs = sum(1 for job in jobs if job["State"] == "COMPLETED")
        failed_jobs = sum(1 for job in jobs if job["State"] == "FAILED")
        total_jobs = successful_jobs + failed_jobs

        success_rate = (successful_jobs / total_jobs * 100) if total_jobs > 0 else 0
        failure_rate = (failed_jobs / total_jobs * 100) if total_jobs > 0 else 0

        backup_distribution = {}
        for vault in vaults:
            region = vault["BackupVaultArn"].split(":")[3]
            backup_distribution[region] = backup_distribution.get(region, 0) + 1

        return {
            "total_snapshots": total_snapshots,
            "snapshot_size_gb": total_size_gb,
            "total_vaults": total_vaults,
            "success_rate": success_rate,
            "failure_rate": failure_rate,
            "backup_distribution": backup_distribution,
        }

    except Exception as e:
        raise Exception(f"Error fetching dashboard metrics: {e}")


def list_aws_regions():
    """
    List all available AWS regions.
    Returns:
        list: List of region names.
    """
    try:
        ec2 = boto3.client("ec2")
        regions = ec2.describe_regions()["Regions"]
        return [region["RegionName"] for region in regions]
    except Exception as e:
        raise Exception(f"Error fetching AWS regions: {e}")
