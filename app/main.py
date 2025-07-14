#!/usr/bin/env python3
"""
Main CLI application entry point.
"""

import argparse
import json
import os
import sys
import requests


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Python CLI Application")
    parser.add_argument(
        "--version", 
        action="version", 
        version="%(prog)s 1.0.0"
    )
    parser.add_argument(
        "--verbose", 
        "-v", 
        action="store_true", 
        help="Enable verbose output"
    )
    parser.add_argument(
        "--report",
        "-r",
        help="Report ID to fetch from HackerOne"
    )
    
    args = parser.parse_args()
    
    if not args.report:
        print("Error: --report argument is required")
        return 1
    
    verbose = args.verbose or os.environ.get("VERBOSE")
    if verbose:
        print("Verbose mode enabled")

    res = requests.get(f'https://hackerone.com/reports/{args.report}.json')
    if res.status_code == 200:
        result_data = res.json()
        # Save result to JSON file automatically
        output_filename = f"report_{args.report}.json"
        with open(output_filename, 'w') as f:
            json.dump(result_data, f, indent=2)
        print(f"Report saved to {output_filename}")
        if verbose:
            print(json.dumps(result_data, indent=2))
    else:
        print("Failed to fetch report")
        if verbose:
            print('Response:' + res.text)
    return 0


if __name__ == "__main__":
    sys.exit(main())