import random
from pydantic import BaseModel
from typing import Optional

class Action(BaseModel):
    fixed_code: str

class Observation(BaseModel):
    buggy_code: str
    task_description: str
    task_id: int
    attempts: int

class Reward(BaseModel):
    score: float
    message: str

TASKS = [
    {
        "id": 1,
        "difficulty": "easy",
        "description": "Fix the function so it correctly returns the sum of two numbers.",
        "buggy_code": "def add(a, b):\n    return a - b",
        "expected_output": "7",
        "test_input": "add(3, 4)",
    },
    {
        "id": 2,
        "difficulty": "medium",
        "description": "Fix the function so it correctly returns the largest number in a list.",
        "buggy_code": "def find_max(lst):\n    max_val = lst[0]\n    for num in lst:\n        if num < max_val:\n            max_val = num\n    return max_val",
        "expected_output": "9",
        "test_input": "find_max([3, 9, 1, 7])",
    },
    {
        "id": 3,
        "difficulty": "hard",
        "description": "Fix the recursive function so it correctly returns the nth Fibonacci number.",
        "buggy_code": "def fib(n):\n    if n == 0:\n        return 0\n    if n == 1:\n        return 1\n    return fib(n-1) + fib(n-3)",
        "expected_output": "8",
        "test_input": "fib(6)",
    },
]

class CodeDebugEnv:
    def __init__(self):
        self.current_task = None
        self.attempts = 0
        self.done = False

    def reset(self, task_id: Optional[int] = None) -> Observation:
        if task_id is not None:
            self.current_task = next((t for t in TASKS if t["id"] == task_id), TASKS[0])
        else:
            self.current_task = random.choice(TASKS)
        self.attempts = 0
        self.done = False
        return Observation(
            buggy_code=self.current_task["buggy_code"],
            task_description=self.current_task["description"],
            task_id=self.current_task["id"],
            attempts=self.attempts,
        )

    def step(self, action: Action):
        if self.done:
            return self.state(), Reward(score=0.0, message="Episode already done. Call reset()."), True, {}
        self.attempts += 1
        score = 0.0
        message = ""
        try:
            local_ns = {}
            exec(action.fixed_code, local_ns)
            result = str(eval(self.current_task["test_input"], local_ns))
            expected = self.current_task["expected_output"]
            if result == expected:
                if self.attempts == 1:
                    score = 1.0
                    message = "Perfect! Fixed in 1 attempt."
                elif self.attempts == 2:
                    score = 0.7
                    message = "Correct! Fixed in 2 attempts."
                else:
                    score = 0.4
                    message = "Correct but took too many attempts."
                self.done = True
            else:
                score = 0.1
                message = f"Wrong output. Got {result}, expected {expected}."
        except Exception as e:
            score = 0.0
            message = f"Code error: {str(e)}"
        return self.state(), Reward(score=score, message=message), self.done, {}

    def state(self) -> Observation:
        return Observation(
            buggy_code=self.current_task["buggy_code"] if self.current_task else "",
            task_description=self.current_task["description"] if self.current_task else "",
            task_id=self.current_task["id"] if self.current_task else 0,
            attempts=self.attempts,
        )