import boto3
import json
from pathlib import Path


def load_plan(file_path):
    """
    Load a backup plan from a JSON file.
    Args:
        file_path (str): Path to the JSON file.
    Returns:
        dict: Loaded backup plan configuration.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Backup plan file not found at {file_path}.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to parse backup plan file at {file_path}.")
        return None


def validate_backup_plan(plan):
    """
    Validate the structure and completeness of a backup plan.
    Args:
        plan (dict): Backup plan configuration.
    Returns:
        bool: True if valid, False otherwise.
    """
    required_keys = ["plan_name", "frequency", "retention_period_days", "regions", "filters"]
    for key in required_keys:
        if key not in plan:
            print(f"Validation Error: Missing required key '{key}'.")
            return False
    return True


def simulate_deployment(plan):
    """
    Simulate the deployment of a backup plan.
    Args:
        plan (dict): Backup plan configuration.
    """
    print("\nSimulating deployment...")
    print(json.dumps(plan, indent=4))
    print("\nSimulation complete. No changes were made.")


def deploy_backup_plan(plan_id, dry_run=False):
    """
    Deploy an AWS Backup plan.
    Args:
        plan_id (str): ID of the backup plan (file name without extension).
        dry_run (bool): Simulate the deployment without making changes.
    """
    try:
        file_path = Path(f"{plan_id}.json")
        backup_plan = load_plan(file_path)

        if not backup_plan:
            print(f"Error: Backup plan '{plan_id}' could not be loaded.")
            return

        if not validate_backup_plan(backup_plan):
            print(f"Error: Backup plan '{plan_id}' is invalid.")
            return

        if dry_run:
            simulate_deployment(backup_plan)
            return

        session = boto3.Session()
        client = session.client("backup")

        # Deploy the backup plan
        response = client.create_backup_plan(
            BackupPlan={
                "BackupPlanName": backup_plan["plan_name"],
                "Rules": [
                    {
                        "RuleName": f"{backup_plan['plan_name']}_rule",
                        "TargetBackupVaultName": "Default",
                        "ScheduleExpression": f"cron({backup_plan['frequency']})",
                        "StartWindowMinutes": 60,
                        "CompletionWindowMinutes": 120,
                        "Lifecycle": {
                            "DeleteAfterDays": backup_plan["retention_period_days"]
                        },
                    }
                ],
            }
        )

        print(f"Backup plan '{plan_id}' deployed successfully!")
        print(json.dumps(response, indent=4))

    except Exception as e:
        print(f"Error deploying backup plan '{plan_id}': {e}")
