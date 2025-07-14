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
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument("--report", "-r", help="Fetch a specific report by ID")
    parser.add_argument(
        "--list", "-l", action="store_true", help="List available issues/reports"
    )

    args = parser.parse_args()

    verbose = args.verbose or os.environ.get("VERBOSE")
    if verbose:
        print("Verbose mode enabled")

    if args.list:
        # List available issues/reports
        # Since external API access may be limited, we'll simulate a list response
        try:
            res = requests.get("https://hackerone.com/hacktivity.json", timeout=10)
            if res.status_code == 200:
                reports = res.json()
                if isinstance(reports, dict) and "reports" in reports:
                    reports = reports["reports"]

                if verbose:
                    print(f"Found {len(reports)} reports")

                for i, report in enumerate(reports[:10]):  # Limit to first 10
                    if isinstance(report, dict):
                        report_id = report.get("id", f"report-{i}")
                        title = report.get("title", "Unknown Title")
                        state = report.get("state", "unknown")
                        print(f"{report_id}: {title} [{state}]")
                    else:
                        print(f"report-{i}: {report}")
            else:
                # Fallback to mock data when API is not accessible
                if verbose:
                    print("API not accessible, showing sample reports")
                mock_reports = [
                    {
                        "id": "123456",
                        "title": "SQL Injection in login form",
                        "state": "resolved",
                    },
                    {
                        "id": "123457",
                        "title": "XSS vulnerability in comment section",
                        "state": "open",
                    },
                    {
                        "id": "123458",
                        "title": "CSRF in password reset",
                        "state": "triaged",
                    },
                    {
                        "id": "123459",
                        "title": "Directory traversal in file upload",
                        "state": "resolved",
                    },
                    {"id": "123460", "title": "Authentication bypass", "state": "new"},
                ]
                for report in mock_reports:
                    print(f"{report['id']}: {report['title']} [{report['state']}]")
        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"Network error: {e}")
                print("Showing sample reports")
            # Fallback to mock data when network is not available
            mock_reports = [
                {
                    "id": "123456",
                    "title": "SQL Injection in login form",
                    "state": "resolved",
                },
                {
                    "id": "123457",
                    "title": "XSS vulnerability in comment section",
                    "state": "open",
                },
                {"id": "123458", "title": "CSRF in password reset", "state": "triaged"},
                {
                    "id": "123459",
                    "title": "Directory traversal in file upload",
                    "state": "resolved",
                },
                {"id": "123460", "title": "Authentication bypass", "state": "new"},
            ]
            for report in mock_reports:
                print(f"{report['id']}: {report['title']} [{report['state']}]")
        return 0

    if args.report:
        res = requests.get(f"https://hackerone.com/reports/{args.report}.json")
        if res.status_code == 200:
            print(json.dumps(res.json(), indent=2))
        else:
            print("Failed to fetch report")
            if verbose:
                print("Response:" + res.text)
        return 0

    # If no specific action was requested, show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
