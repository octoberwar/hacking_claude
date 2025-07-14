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
        help="Output file path to save JSON result"
    )
    
    args = parser.parse_args()
    
    # Validate required arguments
    if not args.report:
        print("Error: --report argument is required", file=sys.stderr)
        parser.print_help()
        return 1
    
    verbose = args.verbose or os.environ.get("VERBOSE")
    if verbose:
        print("Verbose mode enabled")

    res = requests.get(f'https://hackerone.com/reports/{args.report}.json')
    if res.status_code == 200:
        json_data = res.json()
        formatted_json = json.dumps(json_data, indent=2)
        
        # Always print to stdout for backward compatibility
        print(formatted_json)
        
        # Save to file if output path is specified
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
                if verbose:
                    print(f"Result saved to {args.output}")
            except IOError as e:
                print(f"Error saving to file {args.output}: {e}", file=sys.stderr)
                return 1
    else:
        print("Failed to fetch report")
        if verbose:
            print('Response:' + res.text)
    return 0


if __name__ == "__main__":
    sys.exit(main())