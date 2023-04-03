import logging
import os

import httpx

from . import parse

logger = logging.getLogger(__name__)

error_msg = "Sorry I could not process this request"
http_url = f"http://{os.environ['LOCALHOST']}:{os.environ['AGENT_API_DEV_PORT']}/qa-agent/query"
unix_soc_path = f"http://agent/qa-agent/query"
transport = httpx.AsyncHTTPTransport(uds="/var/run/agent.sock")


async def make_unix_socket_call(req: str):
    try:
        async with httpx.AsyncClient(transport=transport, timeout=60) as client:
            response = await client.post(unix_soc_path, json=dict(query=req))
            response.raise_for_status()
            return parse.agent_response(response.json())
    except Exception as e:
        logger.error(f"\nHttpx client raised error: {e}\n")
        return error_msg


async def make_http_call(req: str):
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(http_url, json=dict(query=req))
            response.raise_for_status()
            return parse.agent_response(response.json())
    except Exception as e:
        logger.error(f"\nHttpx client raised error: {e}\n")
        return error_msg
