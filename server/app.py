from fastapi import FastAPI
from app.env import SmartInboxEnv
from app.models import Action

app = FastAPI()
env = SmartInboxEnv()


@app.get("/reset")
@app.post("/reset")
async def reset():
    return await env.reset()


@app.post("/step")
async def step(action: Action):
    return await env.step(action)


@app.get("/state")
async def state():
    return await env.state()

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)