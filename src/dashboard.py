from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from nova.utils.aws_helper import fetch_dashboard_metrics

console = Console()

def display_dashboard():
    """Render the interactive dashboard with AWS metrics."""
    metrics = fetch_dashboard_metrics()

    metrics_table = Table(title="AWS RDS Metrics")
    metrics_table.add_column("Metric", justify="left", style="cyan")
    metrics_table.add_column("Value", justify="right", style="magenta")

    metrics_table.add_row("Total RDS Snapshots", str(metrics["total_snapshots"]))
    metrics_table.add_row("Total Snapshot Size (GB)", f"{metrics['snapshot_size_gb']:.2f}")
    metrics_table.add_row("Total Backup Vaults", str(metrics["total_vaults"]))
    metrics_table.add_row("Backup Success Rate (%)", f"{metrics['success_rate']:.2f}")
    metrics_table.add_row("Backup Failure Rate (%)", f"{metrics['failure_rate']:.2f}")

    backup_distribution_table = Table(title="Backup Distribution by Region")
    backup_distribution_table.add_column("Region", justify="left", style="green")
    backup_distribution_table.add_column("Backups", justify="right", style="yellow")

    for region, count in metrics["backup_distribution"].items():
        backup_distribution_table.add_row(region, str(count))

    dashboard_panel = Panel(
        f"{metrics_table}\n\n{backup_distribution_table}",
        title="AWS Backup Dashboard",
        border_style="blue",
    )

    with Live(dashboard_panel, refresh_per_second=1):
        console.input("Press [bold cyan]Enter[/bold cyan] to refresh or [bold red]Ctrl+C[/bold red] to exit.")


if __name__ == "__main__":
    try:
        display_dashboard()
    except KeyboardInterrupt:
        console.print("\nExiting the dashboard. Goodbye!", style="bold red")
