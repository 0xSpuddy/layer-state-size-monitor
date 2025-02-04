#!/usr/bin/env python3

import os
import time
import csv
from datetime import datetime
import argparse
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def monitor_sizes(dir_a, dir_b, interval, output_file):
    print(f"Starting size monitoring...")
    print(f"Directory A: {dir_a}")
    print(f"Directory B: {dir_b}")
    print(f"Check interval: {interval} seconds")
    print(f"Output file: {output_file}")

    # Create/open CSV file with header
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'dir_a_size', 'dir_b_size', 'difference'])

    while True:
        try:
            # Get sizes
            size_a = get_dir_size(dir_a)
            size_a_gb = (size_a / (1000000000))
            size_a_gb_rounded = round(size_a_gb, 3)
            size_b = get_dir_size(dir_b)
            size_b_gb = (size_b / (1000000000))
            size_b_gb_rounded = round(size_b_gb, 3)
            difference = size_a - size_b
            difference_gb = (difference / (1000000000))
            difference_gb_rounded = round(difference_gb, 3)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Log to stdout
            print(f"[{timestamp}] Dir A: {size_a_gb_rounded} GB, Dir B: {size_b_gb_rounded} GB, Difference: {difference_gb_rounded} GB")

            # Append to CSV
            with open(output_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, size_a_gb_rounded, size_b_gb_rounded, difference_gb_rounded])

            time.sleep(interval)

        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Monitor size difference between two directories')
    parser.add_argument('--dir-a', default=os.getenv('DIRECTORY_A'), help='Path to first directory')
    parser.add_argument('--dir-b', default=os.getenv('DIRECTORY_B'), help='Path to second directory')
    parser.add_argument('--interval', type=int, default=int(os.getenv('CHECK_INTERVAL', 60)), help='Check interval in seconds')
    parser.add_argument('--output', default=os.getenv('OUTPUT_FILE', 'size_difference.csv'), help='Output CSV file path')

    args = parser.parse_args()

    # Validate required parameters
    if not args.dir_a or not args.dir_b:
        print("Error: Both directory paths are required. Set them in .env file or provide as arguments.")
        sys.exit(1)

    monitor_sizes(args.dir_a, args.dir_b, args.interval, args.output)

if __name__ == "__main__":
    main()