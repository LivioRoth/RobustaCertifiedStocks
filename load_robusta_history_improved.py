#!/usr/bin/env python3
"""
Load 3 years of historical Robusta certified stocks data from ICE
With rate limiting and exponential backoff to avoid blocking
"""
import requests
import time
from datetime import datetime, timedelta
import sys

def download_with_retry(url, max_retries=3):
    """Download with exponential backoff on failure"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                return response.content
            elif response.status_code == 429:  # Rate limited
                wait_time = (2 ** attempt) * 5  # 5s, 10s, 20s
                print(f"  ⚠ Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                return None
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return None
    return None

def download_robusta_file(date):
    """Download Robusta stock report for a specific date"""
    date_str = date.strftime('%Y%m%d')
    
    # Try different time patterns (based on observed patterns)
    time_patterns = [
        '103020', '103051', '103118', '103207', '103104', '131152', '103027',
        '103332', '103500', '103733', '103026', '103040', '103445', '103319',
        '103426', '103007', '103359', '102000', '110000', '120000', '130000',
        '140000', '150000'
    ]
    
    for time_pattern in time_patterns:
        url = f"https://www.ice.com/marketdata/publicdocs/liffe/coffee/stock_reports/Stock_Report_RC_{date_str}_{time_pattern}.csv"
        
        content = download_with_retry(url)
        if content:
            filename = f"Stock_Report_RC_{date_str}_{time_pattern}.csv"
            with open(filename, 'wb') as f:
                f.write(content)
            return filename
    
    # Try without time pattern
    url = f"https://www.ice.com/marketdata/publicdocs/liffe/coffee/stock_reports/Stock_Report_RC_{date_str}.csv"
    content = download_with_retry(url)
    if content:
        filename = f"Stock_Report_RC_{date_str}.csv"
        with open(filename, 'wb') as f:
            f.write(content)
        return filename
    
    return None

def main():
    # Calculate date range (3 years back from today)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 3)
    
    print("=" * 80)
    print("ICE ROBUSTA CERTIFIED STOCKS - HISTORICAL DATA LOADER")
    print("=" * 80)
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Rate limiting: 2 second delay between requests")
    print(f"Retry strategy: Exponential backoff on HTTP 429")
    print("=" * 80)
    print()
    
    current_date = start_date
    successful = 0
    failed = 0
    skipped_weekends = 0
    
    while current_date <= end_date:
        # Skip weekends (Robusta data is only published on business days)
        if current_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
            skipped_weekends += 1
            current_date += timedelta(days=1)
            continue
        
        date_str = current_date.strftime('%Y-%m-%d')
        
        filename = download_robusta_file(current_date)
        if filename:
            print(f"✓ {date_str}: {filename}")
            successful += 1
        else:
            print(f"✗ {date_str}: No data available")
            failed += 1
        
        # CRITICAL: Rate limiting to avoid ICE blocking
        time.sleep(2)
        
        current_date += timedelta(days=1)
        
        # Progress update every 30 successful downloads
        if successful > 0 and successful % 30 == 0:
            print()
            print(f"Progress: {successful} files downloaded, {failed} failed, {skipped_weekends} weekends skipped")
            print("=" * 80)
            print()
    
    print()
    print("=" * 80)
    print("DOWNLOAD COMPLETE")
    print("=" * 80)
    print(f"Successful downloads: {successful}")
    print(f"Failed attempts: {failed}")
    print(f"Weekends skipped: {skipped_weekends}")
    print(f"Success rate: {successful / (successful + failed) * 100:.1f}%")
    print()
    print("Next step: Run update_robusta_dashboard.py to generate the dashboard")
    print("=" * 80)

if __name__ == "__main__":
    main()
