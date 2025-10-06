AWS Billing Data Fetcher
A Python script to fetch monthly AWS billing data from Cost Explorer, grouped by service and region, and export it to a CSV file. Costs are rounded to two decimal places to match AWS invoice listings (using UnblendedCost metric).
Features

Fetches monthly cost data for a specified year and month.
Groups costs by AWS Service and Region.
Outputs a CSV with regions as rows and services as columns (defaults to 0.00 for missing values).
Uses AWS Cost Explorer API for accurate, unblended costs (excludes discounts).

Requirements

Python 3.6+ (tested with 3.12).
AWS CLI or boto3 configured with valid credentials (e.g., aws configure).
Access to AWS Cost Explorer (requires appropriate IAM permissions, such as ce:GetCostAndUsage).

Dependencies

boto3 (AWS SDK for Python).
csv and argparse (standard library).
decimal and datetime (standard library).

Install boto3 if needed:
bashpip install boto3
Installation

Clone or download the script.
Ensure your AWS credentials are set up (e.g., via environment variables, IAM roles, or AWS CLI profiles).
The script uses the us-east-1 region for Cost Explorer by default (configurable in code if needed).

Usage
Run the script from the command line, providing the month and year as arguments.
Command-Line Arguments

--month (required): Month number (1-12).
--year (required): Year (e.g., 2025).

Example
bashpython aws_billing_fetcher.py --month 8 --year 2025
This fetches data for August 2025 and generates aws_billing_2025_08.csv.
Output CSV Format

Header: Region followed by sorted service names.
Rows: Sorted regions, with costs (or 0.00) for each service.

Example snippet:
textRegion,Amazon EC2,Amazon S3,Other Services
ap-southeast-1,12.34,5.67,0.00
us-east-1,45.67,23.45,1.23
Notes

Data is fetched for the full month (1st to end-of-month).
Handles errors gracefully (e.g., API failures) and prints status messages.
Costs use ROUND_HALF_UP quantization to match AWS billing precision.
For historical data, ensure the date range is within Cost Explorer's 13-month lookback limit.
Customize the script (e.g., add more groupings or metrics) as needed.

Troubleshooting

Permission Denied: Check IAM policy for Cost Explorer access.
No Data: Verify the date range has billable usage.
Region Issues: Cost Explorer aggregates across regions; adjust region_name in code if using a non-default region.
