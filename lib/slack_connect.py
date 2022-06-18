from lib.constants import *
import json
import logging
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient


def send_msg(client, channel, message):
    """Send a message to a channel in Slack and log it"""
    logging.info(message)
    return client.web_client.chat_postMessage(channel=channel, text=message)

def get_channel_id_by_email(email):
    try:
        request = client.web_client.api_call(f"users.lookupByEmail?email={email}")
        return request['user']['id']
    except Exception as e:
        logging.exception(e)
        return None


with open(SECRETS_JSON, "r") as read_file:
    data = json.load(read_file)
    slack_app_token = data["SLACK_APP_TOKEN"]
    slack_bot_token = data["SLACK_BOT_TOKEN"]

# Initialize SocketModeClient with an app-level token + WebClient
client = SocketModeClient(
    # This app-level token will be used only for establishing a connection
    app_token=slack_app_token,  # xapp-A111-222-xyz
    # You will be using this WebClient for performing Web API calls in listeners
    web_client=WebClient(token=slack_bot_token)  # xoxb-111-222-xyz
)


