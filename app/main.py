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
        help="Enable verbose output"
    )

    
    parser.add_argument(
        "--store",
        "-s",
        help="Store result in json file"
    )
    args = parser.parse_args()
    
    verbose = args.verbose or os.environ.get("VERBOSE")
    if verbose:
        print("Verbose mode enabled")

    res = requests.get(f'https://hackerone.com/reports/{args.report}.json')
    if res.status_code == 200:
        print(json.dumps(res.json(),indent=2))
        if args.store:
            with open(args.store, "w") as f:
                f.write(json.dumps(res.json(), indent=2))
    else:
        print("Failed to fetch report")
        if verbose:
            print('Response:' + res.text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
