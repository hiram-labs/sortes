import os

import httpx
import requests

from . import parse

error_msg = "Sorry I could not process this request"
http_url = f"http://localhost:5001/{os.environ['AGENT_QUERY_ENDPOINT']}"
unix_soc_path = f"http://{os.environ['AGENT_QUERY_ENDPOINT']}"
transport = httpx.HTTPTransport(uds="/var/run/agent.sock")
client = httpx.Client(transport=transport)


def make_unix_socket_call(req: str):
    response = client.post(unix_soc_path, json=dict(query=req))
    if response.status_code == 200:
        return parse.agent_response(response.json())
    else:
        return error_msg


def make_http_call(req: str):
    response = requests.post(http_url, json=dict(query=req))
    if response.status_code == 200:
        return parse.agent_response(response.json())
    else:
        return error_msg
