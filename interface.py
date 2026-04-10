import requests
import os

BASE_URL = "http://127.0.0.1:8000"

TASKS = [
    {"id": "fix_addition_bug", "task_id": 1},
    {"id": "fix_max_finder_bug", "task_id": 2},
    {"id": "fix_fibonacci_bug", "task_id": 3},
]

def solve_task(task):
    print(f"[START] task={task['id']} difficulty=easy")
    
    response = requests.post(f"{BASE_URL}/reset", params={"task_id": task["task_id"]})
    obs = response.json()

    if task["task_id"] == 1:
        fixed = "def add(a, b):\n    return a + b"
    elif task["task_id"] == 2:
        fixed = """def find_max(lst):
    max_val = lst[0]
    for num in lst:
        if num > max_val:
            max_val = num
    return max_val"""
    elif task["task_id"] == 3:
        fixed = """def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)"""

    response = requests.post(f"{BASE_URL}/step", json={"fixed_code": fixed})
    result = response.json()

    print(f"[END] task={task['id']} score={result['reward']['score']}")
    return result['reward']['score']

def main():
    print("Starting baseline inference...")
    scores = []
    for task in TASKS:
        score = solve_task(task)
        scores.append(score)
    
    avg = sum(scores) / len(scores)
    print(f"Average Score: {avg:.2f}")

if __name__ == "__main__":
    main()