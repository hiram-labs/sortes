import logging
import operator
from functools import reduce
from typing import Callable

logger = logging.getLogger(__name__)


async def event(body, say, agent: Callable):
    bot_user_id = reduce(operator.getitem, ["authorizations", 0, "user_id"], body)
    event = reduce(operator.getitem, ["event"], body)
    message = event.get("text")
    agent_response = await agent(message.replace(f"<@{bot_user_id}>", "").strip())
    agent_response = f"{agent_response}"
    return await say(text=agent_response)
