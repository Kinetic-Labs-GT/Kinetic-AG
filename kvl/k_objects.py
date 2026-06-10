# kvl/k_objects.py

import numpy as np
from scipy.ndimage import label

def find_objects(grid, diagonal_connectivity=False):
    """
    Scans a 2D grid and extracts all distinct objects (connected pixels of the same color).
    Returns a list of dictionaries containing object metadata.
    """
    grid = np.array(grid)
    height, width = grid.shape
    detected_objects = []
    
    # Define connectivity matrix (4-way vs 8-way/diagonal)
    if diagonal_connectivity:
        structure = np.ones((3, 3), dtype=int)
    else:
        structure = np.array([[0, 1, 0],
                              [1, 1, 1],
                              [0, 1, 0]])
        
    # We scan each unique color separately (excluding background 0)
    unique_colors = np.unique(grid)
    unique_colors = unique_colors[unique_colors != 0]
    
    for color in unique_colors:
        # Create a binary mask for the current color
        color_mask = (grid == color).astype(int)
        
        # Label connected components for this color
        labeled_mask, num_features = label(color_mask, structure=structure)
        
        for feature_id in range(1, num_features + 1):
            # Isolate the specific object pixels
            obj_indices = np.argwhere(labeled_mask == feature_id)
            
            # Calculate bounding box dimensions
            min_y, min_x = obj_indices.min(axis=0)
            max_y, max_x = obj_indices.max(axis=0)
            
            obj_height = int(max_y - min_y + 1)
            obj_width = int(max_x - min_x + 1)
            
            # Extract the normalized logical mask of the object shape itself
            local_mask = color_mask[min_y:max_y+1, min_x:max_x+1]
            
            detected_objects.append({
                "color": int(color),
                "position": (int(min_y), int(min_x)),
                "dimensions": (obj_height, obj_width),
                "indices": obj_indices.tolist(),
                "mask": local_mask.tolist()
            })
            
    return detected_objects

def filter_by_color(objects, color):
    """Returns a filtered list of objects matching a specific color integer."""
    return [obj for obj in objects if obj["color"] == color]

def filter_by_size(objects, condition="largest"):
    """Filters objects based on the total pixel count size footprint."""
    if not objects:
        return []
    
    sizes = [len(obj["indices"]) for obj in objects]
    
    if condition == "largest":
        max_size = max(sizes)
        return [obj for obj in objects if len(obj["indices"]) == max_size]
    elif condition == "smallest":
        min_size = min(sizes)
        return [obj for obj in objects if len(obj["indices"]) == min_size]
    
    return objects