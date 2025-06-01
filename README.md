# Bat Detection Visualization

This directory contains scripts for processing bat detection data and creating visualizations.

## Scripts

- **batdetect2_view.py**: Main script to consolidate bat detection files and create a visualization. It also opens the visualization in the default web browser.
- **consolidate_detections.py**: Script to consolidate JSON files containing bat detections and adjust timestamps.
- **create_visualization.py**: Script to create an HTML visualization of bat detection data.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### Running batdetect2_view.py

To run the main script, use the following command:

```bash
python batdetect2_view.py <source_dir> [--format <date_format>] [--output <output_file>]
```

- `<source_dir>`: Directory containing the JSON files.
- `--format`: (Optional) Date format for the input filenames. Default is `%Y%m%d_%H%M%S`.
- `--output`: (Optional) Output HTML file name. If not specified, a default name based on the time range will be used.

### Running consolidate_detections.py

To consolidate detection files, use:

```bash
python consolidate_detections.py <source_dir> [--format <date_format>] [--output <output_file>]
```

### Running create_visualization.py

To create a visualization, use:

```bash
python create_visualization.py <input_file> [--output <output_file>]
```

- `<input_file>`: Input JSON file with bat detections.
- `--output`: (Optional) Output HTML file name. Default is `bat_detections.html`. 