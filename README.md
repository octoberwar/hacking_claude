# Python CLI Application

A Python command-line interface application with testing and CI/CD setup.

## Features

- Command-line argument parsing
- Fetch HackerOne reports via API
- JSON output to stdout
- Save JSON results to file automatically
- Verbose output mode
- Version information
- Comprehensive test suite
- GitHub Actions CI/CD pipeline

## Installation

### From Source

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. Install dependencies:
```bash
pip install -e .
```


## Usage

Run the application:
```bash
python app/main.py
```

Or if installed:
```bash
python-cli-app
```

### Command Line Options

- `--version`: Show version information
- `--verbose, -v`: Enable verbose output
- `--report REPORT, -r REPORT`: Report ID to fetch from HackerOne (required)
- `--output OUTPUT, -o OUTPUT`: Output file path to save JSON result
- `--help, -h`: Show help message

### Examples

```bash
# Fetch a report and display JSON to stdout
python app/main.py --report 123456

# Fetch a report with verbose output
python app/main.py --verbose --report 123456

# Fetch a report and save to JSON file
python app/main.py --report 123456 --output report_123456.json

# Fetch a report, save to file, and show verbose output
python app/main.py --verbose --report 123456 --output report_123456.json

# Show version
python app/main.py --version
```

## Development

### Setting up Development Environment

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

4. Format code:
```bash
black app/ tests/
isort app/ tests/
```

5. Lint code:
```bash
flake8 app/ tests/
```

### Project Structure

```
.
├── app/                 # Main application code
│   └── main.py         # CLI entry point
├── tests/              # Test files
│   └── test_main.py    # Main application tests
├── .github/
│   └── workflows/
│       └── test.yml    # GitHub Actions CI/CD
├── .gitignore          # Git ignore file
├── pyproject.toml      # Project configuration and dependencies
└── README.md          # This file
```

## Testing

The project uses pytest for testing. Tests are located in the `tests/` directory.

Run tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run with coverage:
```bash
pytest --cov=app
```

## Continuous Integration

The project uses GitHub Actions for CI/CD. The workflow:

1. Runs tests on Python 3.8, 3.9, 3.10, 3.11, and 3.12
2. Installs dependencies
3. Runs pytest with coverage
4. Uploads coverage to Codecov

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.