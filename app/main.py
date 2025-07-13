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
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: report_{report_id}.json)"
    )
    
    args = parser.parse_args()
    
    # Check if report argument is provided
    if not args.report:
        parser.error("--report argument is required")
    
    verbose = args.verbose or os.environ.get("VERBOSE")
    if verbose:
        print("Verbose mode enabled")

    res = requests.get(f'https://hackerone.com/reports/{args.report}.json')
    if res.status_code == 200:
        json_data = res.json()
        formatted_json = json.dumps(json_data, indent=2)
        
        # Print to stdout (maintain backward compatibility)
        print(formatted_json)
        
        # Determine output filename
        if args.output:
            output_file = args.output
        else:
            output_file = f"report_{args.report}.json"
        
        # Save to file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(formatted_json)
            if verbose:
                print(f"Report saved to: {output_file}")
        except Exception as e:
            print(f"Error saving to file: {e}")
            if verbose:
                print(f"Attempted to save to: {output_file}")
    else:
        print("Failed to fetch report")
        if verbose:
            print('Response:' + res.text)
    return 0


if __name__ == "__main__":
    sys.exit(main())