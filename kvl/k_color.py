# kvl/k_color.py

import numpy as np

def recolor(obj, new_color):
    """
    Creates a copy of an object but swaps out its color code.
    Updates internal pixel indices and mask properties.
    """
    recolored_obj = obj.copy()
    recolored_obj["color"] = int(new_color)
    return recolored_obj

def paint_onto(canvas, obj):
    """
    Stamps an object's mask onto an existing canvas using its structural position anchor.
    Safe boundary checking prevents array clipping crashes.
    """
    canvas = np.array(canvas)
    height, width = canvas.shape
    
    mask = np.array(obj["mask"])
    obj_h, obj_w = mask.shape
    start_y, start_x = obj["position"]
    color = obj["color"]
    
    # Calculate overlap boundaries safely
    canvas_y1 = max(0, start_y)
    canvas_y2 = min(height, start_y + obj_h)
    canvas_x1 = max(0, start_x)
    canvas_x2 = min(width, start_x + obj_w)
    
    mask_y1 = max(0, -start_y)
    mask_y2 = mask_y1 + (canvas_y2 - canvas_y1)
    mask_x1 = max(0, -start_x)
    mask_x2 = mask_x1 + (canvas_x2 - canvas_x1)
    
    # Only paint if the slices are completely valid configurations
    if (canvas_y2 > canvas_y1) and (canvas_x2 > canvas_x1):
        # We find active pixels in the mask component
        active_mask = mask[mask_y1:mask_y2, mask_x1:mask_x2] == 1
        
        # Overlay the object color only onto matching structural indices
        canvas_slice = canvas[canvas_y1:canvas_y2, canvas_x1:canvas_x2]
        canvas_slice[active_mask] = color
        canvas[canvas_y1:canvas_y2, canvas_x1:canvas_x2] = canvas_slice
        
    return canvas.tolist()

def flood_fill_canvas(grid, start_coord, fill_color):
    """
    Performs standard paint-bucket behavior using an optimized BFS loop.
    Fills adjacent matching pixels until a natural boundary block is reached.
    """
    grid = np.array(grid)
    y, x = start_coord
    height, width = grid.shape
    
    # Boundary validation check
    if not (0 <= y < height and 0 <= x < width):
        return grid.tolist()
        
    target_color = grid[y, x]
    if target_color == fill_color:
        return grid.tolist()
        
    # Standard BFS Queue
    queue = [(y, x)]
    grid[y, x] = fill_color
    
    while queue:
        cy, cx = queue.pop(0)
        
        # Check 4-way adjacent neighbors (up, down, left, right)
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < height and 0 <= nx < width:
                if grid[ny, nx] == target_color:
                    grid[ny, nx] = fill_color
                    queue.append((ny, nx))
                    
    return grid.tolist()