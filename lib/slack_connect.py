# from constants import *
import json
import logging
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


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


# Initialize SocketModeClient with an app-level token + WebClient
client = SocketModeClient(
    # This app-level token will be used only for establishing a connection
    app_token= os.environ["SLACK_APP_TOKEN"],  # xapp-A111-222-xyz
    # You will be using this WebClient for performing Web API calls in listeners
    web_client=WebClient(token=os.environ['SLACK_BOT_TOKEN'])  # xoxb-111-222-xyz
)