#!/usr/bin/env python3
"""
CSV to JSON Converter - Web UI

A Flask web application for converting CSV files to JSON with drag-and-drop interface.
"""

import os
import tempfile
import pandas as pd
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify, flash
from werkzeug.utils import secure_filename
import zipfile
import io

app = Flask(__name__)
app.secret_key = 'csv2json_converter_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure upload settings
UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_csv_to_json_data(csv_file, indent=2):
    """
    Convert CSV file to JSON data.
    
    Args:
        csv_file: File object or path
        indent: JSON indentation
        
    Returns:
        tuple: (json_string, filename_without_extension, success)
    """
    try:
        df = pd.read_csv(csv_file)
        json_data = df.to_json(orient='records', indent=indent)
        
        # Get filename without extension
        if hasattr(csv_file, 'filename'):
            filename = Path(csv_file.filename).stem
        else:
            filename = Path(csv_file).stem
            
        return json_data, filename, True
        
    except Exception as e:
        return str(e), None, False

@app.route('/')
def index():
    """Main page with upload interface."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file upload and conversion."""
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files[]')
    converted_files = []
    errors = []
    
    for file in files:
        if file.filename == '':
            continue
            
        if not allowed_file(file.filename):
            errors.append(f"{file.filename}: Not a CSV file")
            continue
        
        # Convert CSV to JSON
        json_data, filename, success = convert_csv_to_json_data(file)
        
        if success:
            converted_files.append({
                'original_name': file.filename,
                'json_name': f"{filename}.json",
                'json_data': json_data
            })
        else:
            errors.append(f"{file.filename}: {json_data}")
    
    if not converted_files and errors:
        return jsonify({'error': 'No files could be converted', 'details': errors}), 400
    
    # If single file, return it directly
    if len(converted_files) == 1:
        file_data = converted_files[0]
        return jsonify({
            'single_file': True,
            'filename': file_data['json_name'],
            'data': file_data['json_data'],
            'errors': errors
        })
    
    # Multiple files - create ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_data in converted_files:
            zip_file.writestr(file_data['json_name'], file_data['json_data'])
    
    zip_buffer.seek(0)
    
    return jsonify({
        'single_file': False,
        'zip_data': zip_buffer.getvalue().hex(),
        'filename': 'converted_files.zip',
        'converted_count': len(converted_files),
        'errors': errors
    })

@app.route('/download/<filename>')
def download_file(filename):
    """Download converted file."""
    # This would be used for individual file downloads if needed
    pass

if __name__ == '__main__':
    # Ensure templates directory exists
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    print("Starting CSV to JSON Converter Web UI...")
    print("Open your browser to: http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)
