from fastapi import FastAPI

from app.api import auth, users

app = FastAPI(title="Smart Planner API")

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}