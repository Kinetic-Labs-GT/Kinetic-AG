# kvl/k_transform.py

import numpy as np

def shift(obj, vector, canvas_dimensions):
    """
    Moves an object by a given (dy, dx) vector.
    Updates the position and re-calculates all internal pixel indices.
    """
    dy, dx = vector
    height, width = canvas_dimensions
    current_y, current_x = obj["position"]
    
    new_y = current_y + dy
    new_x = current_x + dx
    
    # Calculate new pixel indices safely
    new_indices = []
    for y, x in obj["indices"]:
        ny, nx = y + dy, x + dx
        # Boundary protection: only keep pixels that stay on the canvas
        if 0 <= ny < height and 0 <= nx < width:
            new_indices.append([ny, nx])
            
    # Create a copy of the object with updated attributes
    moved_obj = obj.copy()
    moved_obj["position"] = (new_y, new_x)
    moved_obj["indices"] = new_indices
    return moved_obj

def rotate(obj, degrees=90):
    """
    Rotates the object matrix clockwise by 90, 180, or 270 degrees.
    Automatically updates dimensions and mask layout.
    """
    if degrees not in [90, 180, 270]:
        return obj
        
    mask = np.array(obj["mask"])
    k = degrees // 90
    rotated_mask = np.rot90(mask, k=-k) # k=-1 is 90 deg clockwise
    
    # After rotation, update dimensions
    new_height, new_width = rotated_mask.shape
    
    rotated_obj = obj.copy()
    rotated_obj["mask"] = rotated_mask.tolist()
    rotated_obj["dimensions"] = (new_height, new_width)
    
    # Note: 'indices' will need to be remapped when painted onto a canvas
    return rotated_obj

def mirror(obj, axis="vertical"):
    """
    Flips the object horizontally or vertically.
    """
    mask = np.array(obj["mask"])
    if axis == "vertical":
        flipped_mask = np.fliplr(mask) # Flip horizontally along a vertical mirror line
    elif axis == "horizontal":
        flipped_mask = np.flipud(mask) # Flip vertically along a horizontal mirror line
    else:
        return obj
        
    flipped_obj = obj.copy()
    flipped_obj["mask"] = flipped_mask.tolist()
    return flipped_obj