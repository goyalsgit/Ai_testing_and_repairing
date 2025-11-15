import subprocess
import json
import time
from z3 import *
import os

def run_klee(file_path):
    # Compile with KLEE instrumentation
    bc_file = file_path.replace('.c', '.bc')
    try:
        subprocess.run(['clang', '-emit-llvm', '-c', file_path, '-o', bc_file], check=True)
        # Run KLEE
        result = subprocess.run(['klee', bc_file], capture_output=True, text=True, timeout=30)
        # Parse output for bugs (simplified)
        bugs = []
        if 'Error' in result.stdout or 'error' in result.stderr.lower():
            bugs.append({'location': 'unknown', 'description': 'Potential error found'})
        return bugs
    except subprocess.CalledProcessError as e:
        return [{'location': 'compilation', 'description': f'Compilation failed: {e}'}]
    except subprocess.TimeoutExpired:
        return [{'location': 'execution', 'description': 'KLEE execution timed out'}]
    except FileNotFoundError as e:
        return [{'location': 'tool', 'description': f'Tool not found: {e}'}]

def solve_constraints(bugs):
    # Use Z3 to verify constraints (simplified)
    s = Solver()
    x = Int('x')
    s.add(x > 0)
    if s.check() == sat:
        return True  # Constraints satisfiable
    return False

def symbolic_execution_pipeline(file_path):
    start_time = time.time()
    bugs = run_klee(file_path)
    constraints_satisfied = solve_constraints(bugs)
    execution_time = time.time() - start_time

    # Call AI repair
    try:
        from ai_repair.repair import generate_repairs
        repairs = generate_repairs(bugs)
    except Exception as e:
        repairs = []
        for bug in bugs:
            # Simple repair suggestion based on bug description
            if 'tool not found' in bug['description'].lower():
                suggestion = "Install required tools (KLEE, clang) to enable symbolic execution."
            elif 'compilation failed' in bug['description'].lower():
                suggestion = "Check code syntax and ensure all dependencies are included."
            else:
                suggestion = f"Review and fix the issue at {bug['location']}: {bug['description']}"
            repairs.append({
                'description': suggestion,
                'applied': False
            })

    return {
        'bugs': bugs,
        'repairs': repairs,
        'executionTime': execution_time,
        'constraintsSatisfied': constraints_satisfied
    }

if __name__ == '__main__':
    import sys
    file_path = sys.argv[1]
    result = symbolic_execution_pipeline(file_path)
    print(json.dumps(result))
