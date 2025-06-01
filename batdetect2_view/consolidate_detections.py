import json
import os
from datetime import datetime
import glob
import argparse

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

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Consolidate bat detection JSON files and adjust timestamps')
    parser.add_argument('source_dir', help='Source directory containing the JSON files')
    parser.add_argument('--output', '-o', default='consolidated_detections.json',
                      help='Output file name (default: consolidated_detections.json)')
    parser.add_argument('--format', '-f', default='%Y%m%d_%H%M%S',
                      help='''Input filename date format (default: %%Y%%m%%d_%%H%%M%%S)
                      Use %%y for 2-digit year, %%Y for 4-digit year
                      %%m for month, %%d for day
                      %%H for hour, %%M for minute, %%S for second
                      Example: %%Y%%m%%d_%%H%%M%%S for YYYYMMDD_HHMMSS''')
    
    args = parser.parse_args()
    
    # Get all JSON files from source directory
    json_files = glob.glob(os.path.join(args.source_dir, '*.json'))
    
    if not json_files:
        print(f"No JSON files found in {args.source_dir}")
        return
    
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
            base_timestamp = parse_timestamp_from_filename(json_file, args.format)
            
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
    
    # Write consolidated data to new file
    with open(args.output, 'w') as f:
        json.dump(consolidated_data, f, indent=2)
    
    print(f"Consolidated {len(consolidated_data['annotation'])} detections into {args.output}")

if __name__ == "__main__":
    main() 