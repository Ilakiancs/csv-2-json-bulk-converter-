#!/usr/bin/env python3
"""
CSV to JSON Converter

Converts CSV files to JSON format with pretty indentation.
Supports batch processing of multiple files.
"""

import os
import sys
import pandas as pd
from pathlib import Path
import argparse


def create_output_folder(output_folder):
    """Create the output folder if it doesn't exist."""
    Path(output_folder).mkdir(parents=True, exist_ok=True)


def convert_csv_to_json(csv_path, output_folder, indent=2):
    """
    Convert a single CSV file to JSON format.
    
    Args:
        csv_path (str): Path to the CSV file
        output_folder (str): Path to the output folder
        indent (int): JSON indentation spaces
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Create JSON filename
        csv_filename = Path(csv_path).name
        json_filename = Path(csv_filename).stem + '.json'
        json_path = Path(output_folder) / json_filename
        
        # Convert to JSON with pretty formatting
        df.to_json(json_path, orient='records', indent=indent)
        
        print(f"Converted: {csv_filename} -> {json_filename}")
        return True
        
    except Exception as e:
        print(f"Error converting {Path(csv_path).name}: {str(e)}")
        return False


def batch_convert(input_folder="csv_files", output_folder="json_files", indent=2):
    """
    Convert all CSV files in the input folder to JSON format.
    
    Args:
        input_folder (str): Path to folder containing CSV files
        output_folder (str): Path to output folder
        indent (int): JSON indentation spaces
        
    Returns:
        tuple: (successful_count, total_count)
    """
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return 0, 0
    
    create_output_folder(output_folder)
    
    # Get all CSV files
    csv_files = list(Path(input_folder).glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in '{input_folder}' folder.")
        return 0, 0
    
    print(f"Found {len(csv_files)} CSV file(s) to convert:")
    
    successful = 0
    for csv_file in csv_files:
        if convert_csv_to_json(csv_file, output_folder, indent):
            successful += 1
    
    return successful, len(csv_files)


def main():
    """Main function with command line argument support."""
    parser = argparse.ArgumentParser(description="Convert CSV files to JSON format")
    parser.add_argument("-i", "--input", default="csv_files", 
                       help="Input folder containing CSV files (default: csv_files)")
    parser.add_argument("-o", "--output", default="json_files",
                       help="Output folder for JSON files (default: json_files)")
    parser.add_argument("--indent", type=int, default=2,
                       help="JSON indentation spaces (default: 2)")
    parser.add_argument("-f", "--file", 
                       help="Convert a single CSV file instead of folder")
    
    args = parser.parse_args()
    
    print("CSV to JSON Converter")
    print("=" * 30)
    
    if args.file:
        # Convert single file
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' does not exist.")
            sys.exit(1)
        
        create_output_folder(args.output)
        success = convert_csv_to_json(args.file, args.output, args.indent)
        
        if success:
            print("\nConversion completed successfully!")
        else:
            print("\nConversion failed!")
            sys.exit(1)
    else:
        # Batch convert folder
        successful, total = batch_convert(args.input, args.output, args.indent)
        
        print(f"\nConversion completed: {successful}/{total} files successful")
        
        if successful < total:
            sys.exit(1)


if __name__ == "__main__":
    main()
