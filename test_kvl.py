# test_kvl.py

import kvl

# SCENARIO: A puzzle grid with a Red block (color 2) at the top left.
# THE LOGIC TASK: Extract the block, rotate it 90 degrees, paint it Blue (color 1), 
# and move it down into the center of an empty canvas workspace.
input_grid = [
    [2, 2, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

print("--- Starting End-to-End K-VL Pipeline Verification ---")

# 1. Discover objects
detected = kvl.find_objects(input_grid)
target_shape = detected[0]
print(f"Detected initial object. Color: {target_shape['color']}, Anchor Location: {target_shape['position']}")

# 2. Apply Transformations (Rotate, Recolor, Shift)
transformed_shape = kvl.rotate(target_shape, degrees=90)
transformed_shape = kvl.recolor(transformed_shape, new_color=1)
transformed_shape = kvl.shift(transformed_shape, vector=(2, 2), canvas_dimensions=(6, 6))

# 3. Spawn a clean canvas matching the input layout dimensions
clean_canvas = kvl.create_blank_grid_like(input_grid, background_color=0)

# 4. Render the object back onto the canvas
final_output_grid = kvl.paint_onto(clean_canvas, transformed_shape)

print("\nFinal Rendered Grid Matrix Result:")
for row in final_output_grid:
    print(row)