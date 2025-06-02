import json
import os
import glob
from datetime import datetime

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