#!/usr/bin/env python3
"""
Script to parse Robusta CSV files and inject data into HTML dashboard
"""
import csv
import glob
import json
import re
from datetime import datetime

def parse_robusta_csv(filepath):
    """Parse a single Robusta CSV file"""
    data = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Commodity'] == 'RC':  # Skip GrandTotal rows
                data.append({
                    'date': row['CutOffDate'],
                    'port': row['PortId'],
                    'valid': int(row['LotsWithValCert']),
                    'nonTenderable': int(row['LotsNonTend']),
                    'suspended': int(row['LotsSuspended'])
                })
    
    return data

def main():
    # Find all Robusta CSV files
    csv_files = glob.glob('Stock_Report_RC_*.csv')
    
    print(f"Found {len(csv_files)} Robusta CSV files")
    
    # Parse all files
    all_data = []
    for filepath in sorted(csv_files):
        try:
            data = parse_robusta_csv(filepath)
            all_data.extend(data)
            print(f"✓ Parsed: {filepath}")
        except Exception as e:
            print(f"✗ Error parsing {filepath}: {e}")
    
    print(f"\nTotal data points: {len(all_data)}")
    
    # Read the HTML template
    with open('robusta_index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Convert data to JavaScript format
    js_data = json.dumps(all_data, indent=2)
    
    # Inject data into HTML
    html_content = re.sub(
        r'const RAW_DATA = \[\];',
        f'const RAW_DATA = {js_data};',
        html_content
    )
    
    # Write the updated HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Data injected into index.html")
    print(f"✓ Dashboard ready!")

if __name__ == "__main__":
    main()
