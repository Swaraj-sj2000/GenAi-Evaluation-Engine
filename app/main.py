from fastapi import FastAPI
from app.api.routes import runs

app=FastAPI(title="GenAI Eval Engine")

app.include_router(runs.router)