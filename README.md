# Code Debug Environment

A reinforcement learning environment where an AI agent debugs buggy Python code across three difficulty levels.

## Environment Description

The agent receives a buggy Python function and must submit a corrected version. The environment evaluates the fix by executing the code and comparing output against expected results.

## Action Space

| Field | Type | Description |
|-------|------|-------------|
| fixed_code | string | The corrected Python code submitted by the agent |

## Observation Space

| Field | Type | Description |
|-------|------|-------------|
| buggy_code | string | The buggy Python code to fix |
| task_description | string | What the function should do |
| task_id | integer | ID of current task (1, 2, or 3) |
| attempts | integer | Number of attempts made |

## Tasks

| ID | Difficulty | Description |
|----|-----------|-------------|
| 1 | Easy | Fix addition function (wrong operator) |
| 2 | Medium | Fix max finder function (wrong comparison) |
| 3 | Hard | Fix fibonacci function (wrong recursion) |

## Reward Function

- Score 1.0 → Correct fix in 1 attempt
- Score 0.7 → Correct fix in 2 attempts
- Score 0.4 → Correct fix in 3+ attempts
- Score 0.1 → Wrong output
- Score 0.0 → Code error / exception

## Setup Instructions

### Install dependencies
pip install fastapi uvicorn pydantic requests

### Run the server
python -m uvicorn main:app --reload

### Run baseline inference
python inference.py

## Baseline Scores

| Task | Difficulty | Score |
|------|-----------|-------|
| 1 | Easy | 1.0 |
| 2 | Medium | 1.0 |
| 3 | Hard | 1.0 |
| **Average** | | **1.0** |

## API Endpoints

- POST `/reset` - Start new episode
- POST `/step` - Submit fixed code
- GET `/state` - Get current state
- GET `/tasks` - List all tasks
- POST `/baseline` - Run baseline agent
- GET `/grader` - Get grader score