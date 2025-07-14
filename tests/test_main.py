#!/usr/bin/env python3
"""
Unit tests for the CLI application.
"""

import json
import unittest
from io import StringIO
from unittest.mock import Mock, patch

import requests

from app.main import main


class TestCLIApplication(unittest.TestCase):
    """Test cases for the CLI application."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_response_data = {
            "id": "123456",
            "title": "Test Security Report",
            "state": "resolved",
            "severity": "high",
        }

    @patch("sys.argv")
    @patch("builtins.print")
    def test_version_argument(self, mock_print, mock_argv):
        """Test --version argument."""
        mock_argv.__getitem__ = lambda self, index: ["cli_app.py", "--version"][index]
        mock_argv.__len__ = lambda self: 2

        with self.assertRaises(SystemExit) as cm:
            main()

        # argparse exits with code 0 for --version
        self.assertEqual(cm.exception.code, 0)

    @patch("sys.argv")
    @patch("requests.get")
    @patch("builtins.print")
    def test_successful_report_fetch(self, mock_print, mock_get, mock_argv):
        """Test successful report fetching."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: [
            "cli_app.py",
            "--report",
            "123456",
        ][index]
        mock_argv.__len__ = lambda self: 3

        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data
        mock_get.return_value = mock_response

        result = main()

        # Verify the API was called with correct URL
        mock_get.assert_called_once_with("https://hackerone.com/reports/123456.json")

        # Verify the JSON was printed
        expected_json = json.dumps(self.mock_response_data, indent=2)
        mock_print.assert_called_with(expected_json)

        self.assertEqual(result, 0)

    @patch("sys.argv")
    @patch("requests.get")
    @patch("builtins.print")
    def test_failed_report_fetch(self, mock_print, mock_get, mock_argv):
        """Test failed report fetching (non-200 status code)."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: [
            "cli_app.py",
            "--report",
            "999999",
        ][index]
        mock_argv.__len__ = lambda self: 3

        # Mock failed HTTP response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = main()

        # Verify the API was called with correct URL
        mock_get.assert_called_once_with("https://hackerone.com/reports/999999.json")

        # Verify error message was printed
        mock_print.assert_called_with("Failed to fetch report")

        self.assertEqual(result, 0)

    @patch("sys.argv")
    @patch("requests.get")
    @patch("builtins.print")
    def test_verbose_and_report_together(self, mock_print, mock_get, mock_argv):
        """Test verbose flag with report argument."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: [
            "cli_app.py",
            "--verbose",
            "--report",
            "123456",
        ][index]
        mock_argv.__len__ = lambda self: 4

        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data
        mock_get.return_value = mock_response

        result = main()

        # Verify both verbose message and JSON were printed
        expected_calls = [
            unittest.mock.call("Verbose mode enabled"),
            unittest.mock.call(json.dumps(self.mock_response_data, indent=2)),
        ]
        mock_print.assert_has_calls(expected_calls)

        self.assertEqual(result, 0)

    @patch("sys.argv")
    @patch("requests.get")
    @patch("builtins.print")
    def test_short_flags(self, mock_print, mock_get, mock_argv):
        """Test short flag versions (-v, -r)."""
        # Mock command line arguments with short flags
        mock_argv.__getitem__ = lambda self, index: [
            "cli_app.py",
            "-v",
            "-r",
            "123456",
        ][index]
        mock_argv.__len__ = lambda self: 4

        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data
        mock_get.return_value = mock_response

        result = main()

        # Verify both verbose message and JSON were printed
        expected_calls = [
            unittest.mock.call("Verbose mode enabled"),
            unittest.mock.call(json.dumps(self.mock_response_data, indent=2)),
        ]
        mock_print.assert_has_calls(expected_calls)

        self.assertEqual(result, 0)

    @patch("sys.argv")
    @patch("requests.get")
    @patch("builtins.print")
    def test_requests_exception(self, mock_print, mock_get, mock_argv):
        """Test handling of requests exceptions."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: [
            "cli_app.py",
            "--report",
            "123456",
        ][index]
        mock_argv.__len__ = lambda self: 3

        # Mock requests.get to raise an exception
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        with self.assertRaises(requests.exceptions.ConnectionError):
            main()

    @patch("sys.argv")
    @patch("requests.get")
    @patch("builtins.print")
    def test_list_issues_successful(self, mock_print, mock_get, mock_argv):
        """Test successful listing of issues."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: ["cli_app.py", "--list"][index]
        mock_argv.__len__ = lambda self: 2

        # Mock successful HTTP response for list endpoint
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": "111", "title": "Test Issue 1", "state": "open"},
            {"id": "222", "title": "Test Issue 2", "state": "resolved"},
        ]
        mock_get.return_value = mock_response

        result = main()

        # Verify the API was called with correct URL
        mock_get.assert_called_once_with(
            "https://hackerone.com/hacktivity.json", timeout=10
        )

        # Verify the issues were printed
        expected_calls = [
            unittest.mock.call("111: Test Issue 1 [open]"),
            unittest.mock.call("222: Test Issue 2 [resolved]"),
        ]
        mock_print.assert_has_calls(expected_calls)

        self.assertEqual(result, 0)

    @patch("sys.argv")
    @patch("requests.get")
    @patch("builtins.print")
    def test_list_issues_fallback(self, mock_print, mock_get, mock_argv):
        """Test list issues fallback when API returns non-200 status."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: ["cli_app.py", "--list"][index]
        mock_argv.__len__ = lambda self: 2

        # Mock failed HTTP response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = main()

        # Verify mock data was printed
        expected_calls = [
            unittest.mock.call("123456: SQL Injection in login form [resolved]"),
            unittest.mock.call("123457: XSS vulnerability in comment section [open]"),
            unittest.mock.call("123458: CSRF in password reset [triaged]"),
            unittest.mock.call("123459: Directory traversal in file upload [resolved]"),
            unittest.mock.call("123460: Authentication bypass [new]"),
        ]
        mock_print.assert_has_calls(expected_calls)

        self.assertEqual(result, 0)

    @patch("sys.argv")
    @patch("requests.get")
    @patch("builtins.print")
    def test_list_issues_network_error(self, mock_print, mock_get, mock_argv):
        """Test list issues when network error occurs."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: ["cli_app.py", "--list"][index]
        mock_argv.__len__ = lambda self: 2

        # Mock network error
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        result = main()

        # Verify mock data was printed as fallback
        expected_calls = [
            unittest.mock.call("123456: SQL Injection in login form [resolved]"),
            unittest.mock.call("123457: XSS vulnerability in comment section [open]"),
            unittest.mock.call("123458: CSRF in password reset [triaged]"),
            unittest.mock.call("123459: Directory traversal in file upload [resolved]"),
            unittest.mock.call("123460: Authentication bypass [new]"),
        ]
        mock_print.assert_has_calls(expected_calls)

        self.assertEqual(result, 0)

    @patch("sys.argv")
    @patch("requests.get")
    @patch("builtins.print")
    def test_list_issues_verbose(self, mock_print, mock_get, mock_argv):
        """Test list issues with verbose flag."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: [
            "cli_app.py",
            "--list",
            "--verbose",
        ][index]
        mock_argv.__len__ = lambda self: 3

        # Mock network error to trigger fallback
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        result = main()

        # Verify verbose messages and mock data were printed
        expected_calls = [
            unittest.mock.call("Verbose mode enabled"),
            unittest.mock.call("Network error: Network error"),
            unittest.mock.call("Showing sample reports"),
            unittest.mock.call("123456: SQL Injection in login form [resolved]"),
            unittest.mock.call("123457: XSS vulnerability in comment section [open]"),
            unittest.mock.call("123458: CSRF in password reset [triaged]"),
            unittest.mock.call("123459: Directory traversal in file upload [resolved]"),
            unittest.mock.call("123460: Authentication bypass [new]"),
        ]
        mock_print.assert_has_calls(expected_calls)

        self.assertEqual(result, 0)

    @patch("sys.argv")
    @patch("requests.get")
    @patch("builtins.print")
    def test_short_list_flag(self, mock_print, mock_get, mock_argv):
        """Test short flag version (-l) for list."""
        # Mock command line arguments with short flag
        mock_argv.__getitem__ = lambda self, index: ["cli_app.py", "-l"][index]
        mock_argv.__len__ = lambda self: 2

        # Mock network error to trigger fallback
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        result = main()

        # Verify mock data was printed
        expected_calls = [
            unittest.mock.call("123456: SQL Injection in login form [resolved]"),
            unittest.mock.call("123457: XSS vulnerability in comment section [open]"),
            unittest.mock.call("123458: CSRF in password reset [triaged]"),
            unittest.mock.call("123459: Directory traversal in file upload [resolved]"),
            unittest.mock.call("123460: Authentication bypass [new]"),
        ]
        mock_print.assert_has_calls(expected_calls)

        self.assertEqual(result, 0)

    @patch("sys.argv")
    @patch("builtins.print")
    def test_no_arguments_shows_help(self, mock_print, mock_argv):
        """Test that no arguments shows help."""
        # Mock command line arguments with just the script name
        mock_argv.__getitem__ = lambda self, index: ["cli_app.py"][index]
        mock_argv.__len__ = lambda self: 1

        with patch("argparse.ArgumentParser.print_help") as mock_help:
            result = main()
            mock_help.assert_called_once()

        self.assertEqual(result, 0)


class TestIntegration(unittest.TestCase):
    """Integration tests that test the full flow."""

    @patch("requests.get")
    def test_full_workflow_integration(self, mock_get):
        """Test the complete workflow with mocked HTTP requests."""
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "integration_test",
            "title": "Integration Test Report",
        }
        mock_get.return_value = mock_response

        # Capture stdout
        captured_output = StringIO()

        with patch("sys.stdout", captured_output), patch(
            "sys.argv", ["cli_app.py", "--verbose", "--report", "test123"]
        ):
            result = main()

            output = captured_output.getvalue()

            # Verify verbose message is in output
            self.assertIn("Verbose mode enabled", output)

            # Verify JSON is in output
            self.assertIn("integration_test", output)
            self.assertIn("Integration Test Report", output)

            self.assertEqual(result, 0)

    @patch("requests.get")
    def test_list_integration_workflow(self, mock_get):
        """Test the complete list workflow with mocked HTTP requests."""
        # Mock network error to trigger fallback behavior
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        # Capture stdout
        captured_output = StringIO()

        with patch("sys.stdout", captured_output), patch(
            "sys.argv", ["cli_app.py", "--list", "--verbose"]
        ):
            result = main()

            output = captured_output.getvalue()

            # Verify verbose message is in output
            self.assertIn("Verbose mode enabled", output)
            self.assertIn("Network error", output)
            self.assertIn("Showing sample reports", output)

            # Verify sample issues are listed
            self.assertIn("123456: SQL Injection in login form [resolved]", output)
            self.assertIn("123457: XSS vulnerability in comment section [open]", output)
            self.assertIn("123458: CSRF in password reset [triaged]", output)

            self.assertEqual(result, 0)


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
