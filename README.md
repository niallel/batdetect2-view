# Bat Detection Visualization

This directory contains scripts for processing bat detection data and creating visualizations using the output from [batdetect2](https://github.com/macaodha/batdetect2)

## Example output
There is an [example](https://niallel.github.io/batdetect2-view/example.html) you can see [here](https://niallel.github.io/batdetect2-view/example.html), it was from data processed by [batdetect2](https://github.com/macaodha/batdetect2) at 0.3 probability, so doesn't show the detection probabilities below 30%.

## Installation

Install directly from PyPI:

```bash
pip install batdetect2-view
```

To upgrade to the latest version:

```bash
pip install --upgrade batdetect2-view
```

## Usage

To run the visualization tool, use the following command:

```bash
batdetect2_view <source_dir> [--format <date_format>] [--output <output_file>]
```

- `<source_dir>`: Directory containing the JSON files produced by [batdetect2](https://github.com/macaodha/batdetect2)
- `--format`: (Optional) Date format for the input filenames. Default is `%Y%m%d_%H%M%S`.
- `--output`: (Optional) Output HTML file name. If not specified, a default name based on the time range will be used.

The tool will:
1. Consolidate all JSON detection files in the source directory
2. Create an interactive HTML visualization
3. Open the visualization in your default web browser 