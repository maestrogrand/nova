import boto3
from rich.console import Console
from rich.table import Table
import pandas as pd
import json


def fetch_backup_vaults(profile, region=None):
    """
    Fetch all AWS Backup vaults for the specified AWS profile and region.
    Args:
        profile (str): AWS profile name.
        region (str): AWS region filter (optional).
    Returns:
        List[dict]: List of backup vault metadata.
    """
    session = boto3.Session(profile_name=profile, region_name=region)
    client = session.client("backup")

    response = client.list_backup_vaults()
    return response.get("BackupVaultList", [])


def filter_vaults(vaults, min_size=None, region=None):
    """
    Apply filters to the fetched backup vaults.
    Args:
        vaults (list): List of backup vault metadata.
        min_size (int): Minimum size filter for vaults (in GB).
        region (str): AWS region filter.
    Returns:
        List[dict]: Filtered backup vaults.
    """
    filtered = vaults

    if region:
        filtered = [vault for vault in filtered if vault.get("BackupVaultArn", "").endswith(region)]

    if min_size:
        filtered = [vault for vault in filtered if vault.get("NumberOfRecoveryPoints", 0) * 50 >= min_size]

    return filtered


def export_vaults(vaults, file_format, file_path):
    """
    Export the backup vault data to a CSV or JSON file.
    Args:
        vaults (list): List of backup vault metadata.
        file_format (str): Export format ("csv" or "json").
        file_path (str): File path for the export.
    """
    if file_format == "csv":
        df = pd.DataFrame(vaults)
        df.to_csv(file_path, index=False)
    elif file_format == "json":
        with open(file_path, "w") as json_file:
            json.dump(vaults, json_file, indent=4)
    print(f"Exported backup vault data to {file_path}")


def display_vaults(vaults):
    """
    Render the backup vault data in a tabular format in the terminal.
    Args:
        vaults (list): List of backup vault metadata.
    """
    console = Console()
    table = Table(title="AWS Backup Vaults")

    table.add_column("Vault Name", justify="left", style="cyan")
    table.add_column("Recovery Points", justify="right", style="magenta")
    table.add_column("Creation Date", justify="left", style="yellow")
    table.add_column("Region", justify="left", style="green")

    for vault in vaults:
        region = vault.get("BackupVaultArn", "").split(":")[3]
        table.add_row(
            vault["BackupVaultName"],
            str(vault.get("NumberOfRecoveryPoints", 0)),
            vault["CreationDate"].strftime("%Y-%m-%d %H:%M:%S") if "CreationDate" in vault else "N/A",
            region,
        )

    console.print(table)


def list_backup_vaults(region=None, min_size=None, export=None):
    """
    CLI entry point for listing AWS Backup vaults.
    Args:
        region (str): AWS region filter (optional).
        min_size (int): Minimum size filter for vaults (in GB) (optional).
        export (str): Export format ("csv" or "json") (optional).
    """
    try:
        profile = boto3.Session().profile_name
        vaults = fetch_backup_vaults(profile, region)
        filtered_vaults = filter_vaults(vaults, min_size, region)

        if not filtered_vaults:
            print("No backup vaults found matching the specified criteria.")
            return

        if export:
            file_name = f"backup_vaults_{profile}_{region or 'all'}_{export}.csv"
            export_vaults(filtered_vaults, export, file_name)
        else:
            display_vaults(filtered_vaults)

    except Exception as e:
        print(f"Error fetching backup vaults: {e}")
