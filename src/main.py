import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request

from logging_new.logging_config import LOGGING
from logging_new.middlewares import LogRequestInfoMiddleware, SetRequestContextMiddleware
from routers import auth_router, jobs_router, responses_router, user_router

# import os, sys
# current_dir = os.path.dirname(os.path.realpath(__file__))
# main_folder_path = os.path.dirname(current_dir)
# parent_dir = os.path.dirname(main_folder_path)
# sys.path.append(os.path.dirname(parent_dir))
# sys.path.append(current_dir)
# sys.path.append(parent_dir)
# sys.path.append(main_folder_path)

app = FastAPI()
# app.include_router(auth_router)
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
