import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import agent, extract, rank, summarise

if os.environ.get("CURRENT_ENV") == "production":
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
    app = FastAPI(root_path="/agent")
else:
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(agent.router)
app.include_router(rank.router)
app.include_router(extract.router)
app.include_router(summarise.router)
