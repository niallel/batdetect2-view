import json
import os
import glob
import argparse
from datetime import datetime
import webbrowser
from io import StringIO
import sys
from contextlib import redirect_stdout

def parse_timestamp_from_filename(filename, date_format):
    # Extract filename without extension
    base_name = os.path.basename(filename)
    timestamp_str = base_name.split('.')[0]  # Remove extension
    
    try:
        return datetime.strptime(timestamp_str, date_format)
    except ValueError as e:
        raise ValueError(f"Filename '{timestamp_str}' does not match the specified format '{date_format}'. Error: {str(e)}")

def adjust_timestamps(annotations, base_timestamp):
    # Convert base_timestamp to total seconds since epoch
    base_seconds = base_timestamp.timestamp()
    
    # Adjust each annotation's timestamps
    for annotation in annotations:
        annotation['start_time'] += base_seconds
        annotation['end_time'] += base_seconds
    
    return annotations

def consolidate_detections(source_dir, date_format):
    # Get all JSON files from source directory
    json_files = glob.glob(os.path.join(source_dir, '*.json'))
    
    if not json_files:
        raise ValueError(f"No JSON files found in {source_dir}")
    
    # Sort files by timestamp to maintain chronological order
    json_files.sort()
    
    # Initialize consolidated data
    consolidated_data = {
        "annotated": False,
        "annotation": []
    }
    
    # Process each file
    for json_file in json_files:
        try:
            # Parse timestamp from filename
            base_timestamp = parse_timestamp_from_filename(json_file, date_format)
            
            # Read JSON file
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Adjust timestamps in annotations
            adjusted_annotations = adjust_timestamps(data['annotation'], base_timestamp)
            
            # Add to consolidated data
            consolidated_data['annotation'].extend(adjusted_annotations)
            
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")
    
    # Sort all annotations by start_time
    consolidated_data['annotation'].sort(key=lambda x: x['start_time'])
    
    return consolidated_data

def generate_output_filename(data):
    if not data['annotation']:
        return 'batdetect2-visualization.html'
    
    # Get start and end times
    start_time = datetime.fromtimestamp(data['annotation'][0]['start_time'])
    end_time = datetime.fromtimestamp(data['annotation'][-1]['start_time'])
    
    # Format the filename
    return f"batdetect2-{start_time.strftime('%Y%m%d_%H%M%S')}-{end_time.strftime('%Y%m%d_%H%M%S')}.html"

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process bat detection files and create visualization')
    parser.add_argument('source_dir', help='Source directory containing the JSON files')
    parser.add_argument('--format', '-f', default='%Y%m%d_%H%M%S',
                      help='''Input filename date format (default: %%Y%%m%%d_%%H%%M%%S)
                      Use %%y for 2-digit year, %%Y for 4-digit year
                      %%m for month, %%d for day
                      %%H for hour, %%M for minute, %%S for second
                      Example: %%Y%%m%%d_%%H%%M%%S for YYYYMMDD_HHMMSS''')
    parser.add_argument('--output', '-o', default=None, help='Output HTML file name (default: batdetect2-[start]-[end].html)')
    
    args = parser.parse_args()
    
    try:
        # Consolidate detections in memory
        print("Consolidating detection files...")
        consolidated_data = consolidate_detections(args.source_dir, args.format)
        
        # Generate output filename based on time range, unless specified
        output_file = args.output if args.output else generate_output_filename(consolidated_data)
        
        # Import create_visualization here to avoid circular imports
        from create_visualization import create_html_visualization
        
        # Create visualization
        print("Creating visualization...")
        create_html_visualization(consolidated_data, output_file)
        
        # Open in default web browser
        print(f"Opening visualization in browser: {output_file}")
        webbrowser.open('file://' + os.path.abspath(output_file))
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 