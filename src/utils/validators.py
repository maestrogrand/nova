from datetime import datetime
from nova.utils.aws_helper import list_aws_regions


def validate_region(region):
    """
    Validate if the provided region is a valid AWS region.
    Args:
        region (str): AWS region name to validate.
    Returns:
        bool: True if the region is valid, False otherwise.
    """
    try:
        regions = list_aws_regions()
        return region in regions
    except Exception as e:
        print(f"Error validating region: {e}")
        return False


def validate_date(date_string):
    """
    Validate if the provided string is a valid date in YYYY-MM-DD format.
    Args:
        date_string (str): Date string to validate.
    Returns:
        bool: True if the date is valid, False otherwise.
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_backup_plan(plan):
    """
    Validate the structure and content of a backup plan.
    Args:
        plan (dict): Backup plan to validate.
    Returns:
        bool: True if the backup plan is valid, False otherwise.
    """
    required_keys = ["plan_name", "frequency", "retention_period_days", "regions", "filters"]
    for key in required_keys:
        if key not in plan:
            print(f"Validation Error: Missing required key '{key}'.")
            return False

    if not isinstance(plan["regions"], list) or not all(validate_region(r) for r in plan["regions"]):
        print("Validation Error: Invalid or missing AWS regions.")
        return False

    if not isinstance(plan["retention_period_days"], int) or plan["retention_period_days"] <= 0:
        print("Validation Error: Retention period must be a positive integer.")
        return False

    return True
