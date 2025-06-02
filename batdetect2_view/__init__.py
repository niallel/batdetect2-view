"""
batdetect2-view - A visualization tool for batdetect2 output files
"""

from .batdetect2_view import consolidate_detections
from .create_visualization import create_html_visualization
from .cli import main

__version__ = "1.1.0"
__all__ = ['consolidate_detections', 'create_html_visualization', 'main'] 