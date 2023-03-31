import os

import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

qa_agent_endpoint = f"http://{os.environ.get('LOCALHOST')}:{os.environ.get('FAST_API_PORT')}/qa-agent/query"
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

try:
    response = app.client.auth_test()
    bot_user_id = response["user_id"]
except SlackApiError as e:
    print(f"Error: {e}")


@app.event("app_mention")
def handle_app_mention_events(event, say):
    text = event["text"]
    thread_ts = event["thread_ts"] if "thread_ts" in event else event["ts"]
    user_id = event["user"]

    response = requests.post(
        qa_agent_endpoint,
        json=dict(query=text.replace(f"<@{bot_user_id}>", "").strip()),
    )

    if response.status_code == 200:
        response_data = response.json()
        answer_1 = response_data["candidates"][0]["summary"]["best"]
        answer_2 = response_data["candidates"][1]["summary"]["best"]
        label_1 = response_data["candidates"][0]["label"]
        label_2 = response_data["candidates"][1]["label"]
        qualifier = f"These may answer your question:"
        response_text = f"<@{user_id}> {qualifier}\n\n{answer_1}\n{label_1}\n\n\n{answer_2}\n{label_2}\n\n```{str(response_data)}```"
        say(text=response_text, thread_ts=thread_ts)
    else:
        say(f"Request failed with status code {response.status_code}")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
