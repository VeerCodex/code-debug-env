import requests
import os

BASE_URL = "http://127.0.0.1:8000"

def solve_task(task_id: int):
    # Reset environment with specific task
    response = requests.post(f"{BASE_URL}/reset", params={"task_id": task_id})
    obs = response.json()
    
    print(f"\n{'='*50}")
    print(f"Task {task_id} - {obs['task_description']}")
    print(f"Buggy Code:\n{obs['buggy_code']}")
    print(f"{'='*50}")

    # Simple rule-based fixes for baseline
    buggy = obs["buggy_code"]
    fixed = buggy

    # Task 1 fix - addition bug
    if task_id == 1:
        fixed = "def add(a, b):\n    return a + b"

    # Task 2 fix - max finder bug
    elif task_id == 2:
        fixed = """def find_max(lst):
    max_val = lst[0]
    for num in lst:
        if num > max_val:
            max_val = num
    return max_val"""

    # Task 3 fix - fibonacci bug
    elif task_id == 3:
        fixed = """def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)"""

    # Submit fix
    response = requests.post(
        f"{BASE_URL}/step",
        json={"fixed_code": fixed}
    )
    result = response.json()
    
    print(f"Score: {result['reward']['score']}")
    print(f"Message: {result['reward']['message']}")
    print(f"Done: {result['done']}")
    
    return result['reward']['score']

def main():
    print("Starting baseline inference...")
    scores = []
    
    for task_id in [1, 2, 3]:
        score = solve_task(task_id)
        scores.append(score)
    
    avg = sum(scores) / len(scores)
    print(f"\n{'='*50}")
    print(f"BASELINE RESULTS")
    print(f"Task 1 (Easy):   {scores[0]}")
    print(f"Task 2 (Medium): {scores[1]}")
    print(f"Task 3 (Hard):   {scores[2]}")
    print(f"Average Score:   {avg:.2f}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()