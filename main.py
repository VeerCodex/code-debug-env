from fastapi import FastAPI
from models import Action, Observation, CodeDebugEnv, TASKS

app = FastAPI(title="Code Debug Environment")
env = CodeDebugEnv()

@app.post("/reset")
def reset(task_id: int = None):
    obs = env.reset(task_id=task_id)
    return obs

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()

@app.get("/tasks")
def get_tasks():
    return {"tasks": TASKS}

@app.get("/grader")
def grader():
    if env.current_task is None:
        return {"score": 0.0, "message": "No task running."}
    return {"score": 0.0, "message": "Episode not finished yet."}

@app.post("/baseline")
def baseline():
    results = []
    for task in TASKS:
        env.reset(task_id=task["id"])
        # Dummy baseline - just returns buggy code as-is
        action = Action(fixed_code=task["buggy_code"])
        obs, reward, done, info = env.step(action)
        results.append({
            "task_id": task["id"],
            "difficulty": task["difficulty"],
            "score": reward.score,
            "message": reward.message
        })
    return {"baseline_results": results}

@app.get("/")
def root():
    return {"message": "Code Debug Environment is running!"}