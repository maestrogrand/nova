import click
from nova.profile_selector import select_profile
from nova.report_generator.rds_snapshots import list_rds_snapshots
from nova.report_generator.backup_vaults import list_backup_vaults
from nova.backup_manager.create_plan import create_backup_plan
from nova.backup_manager.deploy_plan import deploy_backup_plan


@click.group()
@click.version_option(version="1.0.0", prog_name="Nova")
def cli():
    """Nova: AWS RDS Backup Management Tool"""
    pass


@cli.command()
def profile_switch():
    """Switch AWS profiles for the current session."""
    profile = select_profile()
    if profile:
        click.echo(f"Successfully switched to profile: {profile}")
    else:
        click.echo("Failed to select a profile. Please try again.")


@cli.command()
@click.option("--region", default=None, help="Filter snapshots by AWS region.")
@click.option("--instance", default=None, help="Filter snapshots by RDS instance.")
@click.option("--date", default=None, help="Filter snapshots by creation date (YYYY-MM-DD).")
@click.option("--export", type=click.Choice(["csv", "json"]), help="Export data to CSV or JSON.")
def list_snapshots(region, instance, date, export):
    """List RDS snapshots with optional filtering and export options."""
    list_rds_snapshots(region=region, instance=instance, date=date, export=export)


@cli.command()
@click.option("--region", default=None, help="Filter backup vaults by AWS region.")
@click.option("--min-size", default=None, type=int, help="Filter vaults by minimum size (in GB).")
@click.option("--export", type=click.Choice(["csv", "json"]), help="Export data to CSV or JSON.")
def list_vaults(region, min_size, export):
    """List AWS Backup vaults with optional filtering and export options."""
    list_backup_vaults(region=region, min_size=min_size, export=export)


@cli.command()
@click.option("--file", default=None, type=click.Path(), help="Path to JSON file for plan parameters.")
def create_backup(file):
    """Create a new backup plan interactively or using a JSON file."""
    create_backup_plan(file)


@cli.command()
@click.option("--plan-id", required=True, help="ID of the backup plan to deploy.")
@click.option("--dry-run", is_flag=True, help="Simulate deployment without making changes.")
def deploy_backup(plan_id, dry_run):
    """Deploy an existing backup plan."""
    deploy_backup_plan(plan_id=plan_id, dry_run=dry_run)


if __name__ == "__main__":
    cli()
