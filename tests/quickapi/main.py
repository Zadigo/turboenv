from fastapi import FastAPI
from src.turboenv.main import TurboEnv


app = FastAPI()

env = TurboEnv()
env.load_envs('.env')
env.conditional('DEBUG').to_be('True')

DEBUG = env.boolean('DEBUG')

print(DEBUG)

@app.get("/")
async def root():
    return {"message": "Hello World"}
