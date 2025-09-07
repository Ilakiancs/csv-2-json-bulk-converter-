# CSV to JSON Converter

Convert CSV files to JSON format with pretty indentation.

## Features

- Command-line converter for batch processing
- Web UI for drag-and-drop file conversion
- JSON output as array of objects with pretty formatting
- Automatic output folder creation

## Requirements

- Python 3.6+
- pandas
- flask (for web UI)

## Installation

```bash
pip install pandas flask
```

## Usage

### Command Line Version
1. Place CSV files in `csv_files/` folder
2. Run: `python csv_to_json_converter.py`
3. Find converted files in `json_files/` folder

### Web UI Version
1. Run: `python ui_converter.py`
2. Open browser to `http://localhost:5000`
3. Drag and drop CSV files to convert
4. Download converted JSON files

## Output Format

Input CSV becomes an array of JSON objects with 2-space indentation.
# csv-2-json-bulk-converter-
