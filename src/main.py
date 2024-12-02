import logging
import logging.config
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request

from routers import auth_router, jobs_router, responses_router, user_router
from src.logging.logging_config import LOGGING
from src.logging.middlewares import LogRequestInfoMiddleware, SetRequestContextMiddleware

app = FastAPI()
app.include_router(auth_router)
# app.include_router(user_router)
app.include_router(jobs_router)
app.include_router(responses_router)
app.add_middleware(LogRequestInfoMiddleware)
app.add_middleware(SetRequestContextMiddleware)


@app.get("/")
def hello():
    """
    Здесь должно быть крутое промо
    """
    return {"message": "Башкирский баш хантер приветствует тебя"}


if __name__ == "__main__":
    logging.config.dictConfig(LOGGING)
    uvicorn.run("main:app", port=8080, reload=True, log_level=logging.INFO, log_config=LOGGING)
