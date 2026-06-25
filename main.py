from fastapi import FastAPI
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

app = FastAPI()

@app.get("/health")
async def health():
    """Health check endpoint for Kubernetes liveness and readiness probes."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 503

@app.get("/")
async def root(id: int):
    with engine.connect() as connection:
        result = connection.execute(text("""SELECT name from public."TestTable" WHERE id = :id"""), {"id": id})
        name = result.scalar()

    return {"message": name}