# verify_engine.py

import json
import traceback
import numpy as np
import kvl

def verify_solution(task_file_path, solution_code_str):
    """
    Sandboxes and executes a Python code string against all training pairs of an ARC task.
    Returns True only if the code runs error-free and matches 100% of the target outputs.
    """
    # 1. Load the target puzzle data
    with open(task_file_path, "r") as f:
        task_data = json.load(f)
        
    # 2. Build the sandboxed context environment
    # We explicitly expose the K-VL library and NumPy to the dynamic execution scope
    sandbox_globals = {
        "kvl": kvl,
        "np": np,
        "__builtins__": __builtins__
    }
    
    # 3. Compile and execute the raw text string to inject the 'solve' function
    try:
        exec(solution_code_str, sandbox_globals)
        if "solve" not in sandbox_globals:
            print("[-] Verification Failed: Code string does not contain a defined 'solve(grid)' function.")
            return False
        solve_func = sandbox_globals["solve"]
    except Exception as e:
        print("[-] Verification Failed: Syntax or compilation error inside the generated script.")
        print(f"Error Details: {e}")
        return False

    print(f"--- Evaluating Solution Against {len(task_data['train'])} Training Examples ---")
    
    # 4. Iteratively process every demonstration pair
    for idx, example in enumerate(task_data["train"]):
        input_grid = example["input"]
        expected_output = example["output"]
        
        try:
            # Execute the generated logic code
            predicted_output = solve_func(input_grid)
            
            # Use NumPy array comparison for strict matrix equality checks
            if np.array_equal(np.array(predicted_output), np.array(expected_output)):
                print(f"    [+] Example {idx + 1}: Passed flawlessly.")
            else:
                print(f"    [-] Example {idx + 1}: Failed. Output grid structure or pixels mismatch.")
                return False
                
        except Exception as e:
            print(f"    [-] Example {idx + 1}: CRASHED during active execution loops.")
            print(f"    Exception Trace: {e}")
            # Uncomment line below if you need to debug deeply during synthetic generation
            # traceback.print_exc()
            return False

    print("\n[SUCCESS] Code block verified! Safe for execution on the hidden test grid.")
    return True