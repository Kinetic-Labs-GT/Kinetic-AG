# kvl/k_space.py

import numpy as np

def get_dimensions(grid):
    """Returns the (height, width) of a given grid matrix."""
    return np.array(grid).shape

def create_blank_grid(height, width, background_color=0):
    """Generates a blank 2D matrix filled completely with a background color."""
    return np.full((height, width), background_color, dtype=int).tolist()

def create_blank_grid_like(grid, background_color=0):
    """Generates a blank canvas that perfectly matches the sizing of a reference grid."""
    height, width = get_dimensions(grid)
    return create_blank_grid(height, width, background_color)