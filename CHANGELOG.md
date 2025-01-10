Changelog
All notable changes to this project will be documented in this file. The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

[1.0.0] - 2025-01-10
Added
Interactive Dashboard:

Display RDS snapshot metrics (total count, total size).
Display AWS Backup vault metrics (total count, success/failure rates, backup distribution by region).
Integrated rich for visualizations.
AWS Profile Selector:

List and select AWS profiles from the ~/.aws/credentials file.
Validate profiles and provide fallback for manual credential input.
Report Generation:

Generate RDS snapshot reports with filters (region, instance, date).
Export snapshot reports to CSV or JSON.
Generate AWS Backup vault reports with filters (region, size).
Export vault reports to CSV or JSON.
Backup Plan Management:

Create new backup plans interactively or using JSON configurations.
Deploy backup plans with or without dry-run mode.
Validate backup plans for completeness and correctness.
Command-Line Interface (CLI):

profile-switch: Switch AWS profiles for the session.
list-snapshots: List and filter RDS snapshots.
list-vaults: List and filter AWS Backup vaults.
create-backup: Create a new backup plan.
deploy-backup: Deploy an existing backup plan.
Logging:

Log all operations (e.g., backup plan creation, deployment, report generation).
Log errors and debugging information to ~/.nova/logs/nova.log.
Utilities:

AWS helper functions for fetching metrics and validating connections.
Validators for regions, dates, and backup plans.
[Unreleased]
Planned
Support for Additional AWS Services:

Add S3 and EC2 backup management.
CloudWatch Integration:

Monitor real-time backup job metrics and alerts.
Auto-Refresh Dashboard:

Enable automatic refresh for the interactive dashboard.
Customizable Metrics:

Allow users to define and display custom dashboard metrics.
Bulk Operations:

Support batch processing for snapshot and vault exports.
Template for Future Releases
Added
Briefly describe new features or enhancements.
Changed
Describe any modifications or improvements to existing features.
Deprecated
List any features or functionality that are no longer recommended for use.
Removed
Describe features that have been removed from the project.
Fixed
Detail any bug fixes or resolved issues.
Note: For detailed information on how to contribute, see the CONTRIBUTING.md file.

