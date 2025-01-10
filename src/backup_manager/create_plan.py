import json
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog
from pathlib import Path


def create_backup_plan_interactive():
    """
    Create a backup plan interactively.
    Returns:
        dict: Backup plan configuration.
    """
    print("Creating a new AWS Backup plan interactively...\n")

    # Plan name
    plan_name = prompt("Enter a unique backup plan name: ")

    # Frequency
    frequency_options = [("Daily", "daily"), ("Weekly", "weekly")]
    frequency = radiolist_dialog(
        title="Backup Frequency",
        text="Select the backup frequency:",
        values=frequency_options,
    ).run()

    # Retention period
    retention = prompt("Enter the retention period (in days): ", default="30")

    # AWS regions
    regions = prompt("Enter the AWS regions for backups (comma-separated): ")

    # Filters (tags or instances)
    filter_type = radiolist_dialog(
        title="Backup Filters",
        text="Select a filter type for backups:",
        values=[("Tags", "tags"), ("Instances", "instances")],
    ).run()

    filters = {}
    if filter_type == "tags":
        key = prompt("Enter the tag key: ")
        value = prompt("Enter the tag value: ")
        filters["tags"] = {key: value}
    elif filter_type == "instances":
        instances = prompt("Enter the instance names (comma-separated): ")
        filters["instances"] = instances.split(",")

    # Construct the backup plan
    backup_plan = {
        "plan_name": plan_name,
        "frequency": frequency,
        "retention_period_days": int(retention),
        "regions": regions.split(","),
        "filters": filters,
    }

    print("\nBackup plan created successfully!")
    return backup_plan


def save_plan_to_file(plan, file_path):
    """
    Save the backup plan to a JSON file.
    Args:
        plan (dict): Backup plan configuration.
        file_path (str): Path to save the file.
    """
    with open(file_path, "w") as file:
        json.dump(plan, file, indent=4)
    print(f"Backup plan saved to {file_path}")


def create_backup_plan(file=None):
    """
    Main function to create a backup plan interactively or from a JSON file.
    Args:
        file (str): Path to JSON file for backup plan parameters (optional).
    """
    try:
        if file:
            # Load from JSON file
            with open(file, "r") as json_file:
                backup_plan = json.load(json_file)
            print(f"Loaded backup plan from {file}")
        else:
            # Create interactively
            backup_plan = create_backup_plan_interactive()

        # Save the plan
        file_path = f"{backup_plan['plan_name']}.json"
        save_plan_to_file(backup_plan, file_path)

    except Exception as e:
        print(f"Error creating backup plan: {e}")
