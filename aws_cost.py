import boto3
import csv
import argparse
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta

# Create a Cost Explorer client
ce_client = boto3.client('ce', region_name='us-east-1')

def fetch_billing_data(start_date, end_date):
    """
    Fetch the billing data from AWS Cost Explorer for the specified date range.
    Uses UnblendedCost to match the AWS invoice listing (list rates minus discounts).
    """
    try:
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'DIMENSION', 'Key': 'REGION'}
            ]
        )
        return response
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def process_and_save_to_csv(response, file_name):
    """
    Process the AWS Cost Explorer response and save the data into CSV format,
    rounding each cost to two decimal places to match AWS billing.
    Rows are regions, columns are services.
    """
    regions = set()
    services = set()
    data_entries = []

    if response:
        for result in response.get('ResultsByTime', []):
            for group in result.get('Groups', []):
                service = group['Keys'][0]
                region = group['Keys'][1]
                amount_raw = Decimal(group['Metrics']['UnblendedCost']['Amount'])
                # Round per AWS billing logic
                amount = amount_raw.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

                regions.add(region)
                services.add(service)
                data_entries.append((region, service, amount))

    regions = sorted(regions)
    services = sorted(services)

    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ['Region'] + services
        writer.writerow(header)

        for region in regions:
            row = [region]
            for service in services:
                cell = ''
                for entry in data_entries:
                    if entry[0] == region and entry[1] == service:
                        cell = f"{entry[2]:.2f}"
                        break
                if not cell:
                    cell = "0.00"
                row.append(cell)
            writer.writerow(row)

    print(f"CSV file '{file_name}' has been created.")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fetch AWS billing data for a specific month/year")
    parser.add_argument("--month", type=int, required=True, help="Month number (1-12)")
    parser.add_argument("--year", type=int, required=True, help="Year (e.g., 2025)")
    args = parser.parse_args()

    # Calculate first and last day of the selected month
    first_day = datetime(args.year, args.month, 1)
    if args.month == 12:
        first_day_next = datetime(args.year + 1, 1, 1)
    else:
        first_day_next = datetime(args.year, args.month + 1, 1)

    start_date = first_day.strftime('%Y-%m-%d')
    end_date = first_day_next.strftime('%Y-%m-%d')

    # File name e.g. aws_billing_2025_08.csv
    file_name = f"aws_billing_{args.year}_{args.month:02d}.csv"

    response = fetch_billing_data(start_date, end_date)
    if response:
        process_and_save_to_csv(response, file_name)


if __name__ == '__main__':
    main()
