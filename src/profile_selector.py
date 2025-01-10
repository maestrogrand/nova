import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from configparser import ConfigParser
from pathlib import Path
from prompt_toolkit.shortcuts import radiolist_dialog

AWS_CREDENTIALS_PATH = Path("~/.aws/credentials").expanduser()

def list_profiles():
    """List available AWS profiles from the credentials file."""
    if not AWS_CREDENTIALS_PATH.exists():
        raise FileNotFoundError(f"Credentials file not found at {AWS_CREDENTIALS_PATH}")
    
    config = ConfigParser()
    config.read(AWS_CREDENTIALS_PATH)
    return config.sections()


def validate_profile(profile_name):
    """Validate the selected AWS profile by attempting to create a session."""
    try:
        session = boto3.Session(profile_name=profile_name)
        client = session.client("sts")
        client.get_caller_identity()
        return True
    except (NoCredentialsError, PartialCredentialsError):
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def select_profile():
    """Interactive profile selection."""
    try:
        profiles = list_profiles()
        if not profiles:
            raise ValueError("No profiles found in AWS credentials file.")
        
        profile_choice = radiolist_dialog(
            title="AWS Profile Selector",
            text="Select an AWS profile for this session:",
            values=[(profile, profile) for profile in profiles],
        ).run()

        if profile_choice is None:
            print("Profile selection canceled.")
            return None

        if validate_profile(profile_choice):
            print(f"Profile '{profile_choice}' selected successfully.")
            return profile_choice
        else:
            print(f"Invalid profile: {profile_choice}. Please check your credentials.")
            return None

    except FileNotFoundError as e:
        print(e)
        return None


def manual_profile_input():
    """Fallback to manually input AWS credentials."""
    print("Manual AWS profile input:")
    aws_access_key = input("AWS Access Key ID: ")
    aws_secret_key = input("AWS Secret Access Key: ")
    aws_region = input("AWS Region (e.g., us-east-1): ")

    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    try:
        client = session.client("sts")
        client.get_caller_identity()
        print("Manual credentials validated successfully.")
        return session
    except Exception as e:
        print(f"Failed to validate manual credentials: {e}")
        return None


if __name__ == "__main__":
    profile = select_profile()
    if profile is None:
        print("Falling back to manual credentials input.")
        manual_profile_input()
