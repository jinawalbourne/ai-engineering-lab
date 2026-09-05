from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.database import check_database_connection


app = FastAPI(title="AI Engineering Lab")


@app.get("/health", response_model=None)
def health_check():
    if check_database_connection():
        return {"status": "healthy"}

    return JSONResponse(
        status_code=503,
        content={"status": "unhealthy"},
    )
