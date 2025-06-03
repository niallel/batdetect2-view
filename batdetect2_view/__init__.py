"""
batdetect2-view - A visualization tool for batdetect2 output files
"""

__version__ = "1.4.1"

from .batdetect2_view import consolidate_detections
from .create_visualization import create_html_visualization
from .cli import main

__all__ = ['consolidate_detections', 'create_html_visualization', 'main'] 