import logging
import os

from slack_bolt.adapter.asgi.async_handler import AsyncSlackRequestHandler
from slack_bolt.async_app import AsyncApp

from .handler import on_direct_message, on_mention
from .utils import agent

if os.environ.get("CURRENT_ENV") == "production":
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
    agent = agent.make_unix_socket_call
    app = AsyncApp(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    )
else:
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)
    agent = agent.make_http_call
    app = AsyncApp(
        token=os.environ.get("SLACK_BOT_DEV_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_DEV_SECRET"),
    )


@app.event("app_mention")
async def handle_mention(body, say):
    await on_mention.event(body, say, agent=agent)


@app.event("message")
async def handle_message(body, say):
    await on_direct_message.event(body, say, agent=agent)


bot = AsyncSlackRequestHandler(app)
