import boto3
from rich.console import Console
from rich.table import Table
import pandas as pd
import json
from datetime import datetime


def fetch_snapshots(profile, region=None):
    """
    Fetch all RDS snapshots for the specified AWS profile and region.
    Args:
        profile (str): AWS profile name.
        region (str): AWS region filter (optional).
    Returns:
        List[dict]: List of snapshots metadata.
    """
    session = boto3.Session(profile_name=profile, region_name=region)
    client = session.client("rds")

    snapshots = []
    paginator = client.get_paginator("describe_db_snapshots")
    for page in paginator.paginate():
        snapshots.extend(page["DBSnapshots"])
    return snapshots


def filter_snapshots(snapshots, region=None, instance=None, date=None):
    """
    Apply filters to the fetched RDS snapshots.
    Args:
        snapshots (list): List of snapshot metadata.
        region (str): AWS region filter.
        instance (str): RDS instance name filter.
        date (str): Snapshot creation date filter (YYYY-MM-DD).
    Returns:
        List[dict]: Filtered snapshots.
    """
    filtered = snapshots

    if region:
        filtered = [snap for snap in filtered if snap["DBInstanceIdentifier"] == instance]

    if instance:
        filtered = [snap for snap in filtered if snap["DBInstanceIdentifier"] == instance]

    if date:
        date_filter = datetime.strptime(date, "%Y-%m-%d")
        filtered = [
            snap
            for snap in filtered
            if datetime.strptime(snap["SnapshotCreateTime"], "%Y-%m-%dT%H:%M:%S.%fZ").date() == date_filter.date()
        ]

    return filtered


def export_snapshots(snapshots, file_format, file_path):
    """
    Export the snapshot data to a CSV or JSON file.
    Args:
        snapshots (list): List of snapshot metadata.
        file_format (str): Export format ("csv" or "json").
        file_path (str): File path for the export.
    """
    if file_format == "csv":
        df = pd.DataFrame(snapshots)
        df.to_csv(file_path, index=False)
    elif file_format == "json":
        with open(file_path, "w") as json_file:
            json.dump(snapshots, json_file, indent=4)
    print(f"Exported snapshot data to {file_path}")


def display_snapshots(snapshots):
    """
    Render the snapshot data in a tabular format in the terminal.
    Args:
        snapshots (list): List of snapshot metadata.
    """
    console = Console()
    table = Table(title="RDS Snapshots")

    table.add_column("Snapshot ID", justify="left", style="cyan")
    table.add_column("Instance Name", justify="left", style="green")
    table.add_column("Size (GB)", justify="right", style="magenta")
    table.add_column("Creation Time", justify="left", style="yellow")
    table.add_column("Region", justify="left", style="blue")

    for snap in snapshots:
        table.add_row(
            snap["DBSnapshotIdentifier"],
            snap["DBInstanceIdentifier"],
            str(snap["AllocatedStorage"]),
            snap["SnapshotCreateTime"],
            snap["AvailabilityZone"],
        )

    console.print(table)


def list_rds_snapshots(region=None, instance=None, date=None, export=None):
    """
    CLI entry point for listing RDS snapshots.
    Args:
        region (str): AWS region filter (optional).
        instance (str): RDS instance name filter (optional).
        date (str): Snapshot creation date filter (optional).
        export (str): Export format ("csv" or "json") (optional).
    """
    try:
        profile = boto3.Session().profile_name
        snapshots = fetch_snapshots(profile, region)
        filtered_snapshots = filter_snapshots(snapshots, region, instance, date)

        if not filtered_snapshots:
            print("No snapshots found matching the specified criteria.")
            return

        if export:
            file_name = f"rds_snapshots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export}"
            export_snapshots(filtered_snapshots, export, file_name)
        else:
            display_snapshots(filtered_snapshots)

    except Exception as e:
        print(f"Error fetching RDS snapshots: {e}")
