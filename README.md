---
title: Code Debug Env
emoji: 🐛
colorFrom: blue
colorTo: red
sdk: docker
app_file: app.py
pinned: false
---

# Code Debug Environment

A reinforcement learning environment where an AI agent debugs buggy Python code across three difficulty levels.

## Action Space
- fixed_code: string — The corrected Python code

## Observation Space
- buggy_code, task_description, task_id, attempts

## Tasks
1. Easy — Fix addition bug
2. Medium — Fix max finder bug  
3. Hard — Fix fibonacci bug

## Setup
pip install fastapi uvicorn pydantic requests
python -m uvicorn main:app --reload

## Baseline Scores
| Task | Score |
|------|-------|
| Easy | 1.0 |
| Medium | 1.0 |
| Hard | 1.0 |