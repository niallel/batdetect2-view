import argparse
import os
import webbrowser
import sys
from datetime import datetime
from .batdetect2_view import consolidate_detections
from .create_visualization import create_html_visualization
from . import __version__

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
    parser.add_argument('--version', '-v', action='version',
                      version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    try:
        # Consolidate detections in memory
        print("Consolidating detection files...")
        consolidated_data = consolidate_detections(args.source_dir, args.format)
        
        # Generate output filename based on time range, unless specified
        output_file = args.output if args.output else generate_output_filename(consolidated_data)
        
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