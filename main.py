from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from dotenv import load_dotenv

import os
import config

load_dotenv('tokens.env')

SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

app = App(token=SLACK_BOT_TOKEN)

@app.command(config.JOIN_COMMAND)
def handle_join_request(ack, command, client):
    ack()
    requester_id = command["user_id"]
    send_join_request(requester_id, client)

if config.ENABLE_WORKFLOW_COMMAND:
    @app.command(config.WORKFLOW_COMMAND)
    def handle_workflow_request(ack, say, client):
        ack()

        say(
            text=config.WORKFLOW_TEXT.format(user_id=config.USER_ID),
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": config.WORKFLOW_TEXT.format(user_id=config.USER_ID)
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": config.JOIN_REQUEST_BUTTON_TEXT,
                                "emoji": True
                            },
                            "style": config.JOIN_BUTTON_STYLE,
                            "value": "trigger_join",
                            "action_id": config.WORKFLOW_JOIN_ACTION_ID
                        }
                    ]
                }
            ]
        )

    @app.action(config.WORKFLOW_JOIN_ACTION_ID)
    def handle_workflow_event(ack, body, client):
        ack()
        requester_id = body["user"]["id"]
        send_join_request(requester_id, client)

@app.action(config.ACCEPT_ACTION_ID)
def handle_joinrequest_accept(ack, body, client):
    ack()

    requester_id = body["actions"][0]["value"]

    try:
        client.conversations_invite(
            channel=config.CHANNEL_ID,
            users=requester_id
        )

        client.chat_update(
            channel=body["channel"]["id"],
            ts=body["message"]["ts"],
            text=config.INVITE_SUCCESS_MESSAGE.format(requester_id=requester_id, channel_id=config.CHANNEL_ID),
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": config.INVITE_SUCCESS_MESSAGE.format(requester_id=requester_id, channel_id=config.CHANNEL_ID)
                    }
                }
            ]
        )
    except Exception as e:
        client.chat_postMessage(
            channel=config.USER_ID,
            text=config.INVITE_FAILURE_MESSAGE.format(requester_id=requester_id, channel_id=config.CHANNEL_ID),
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": config.INVITE_FAILURE_MESSAGE.format(requester_id=requester_id, channel_id=config.CHANNEL_ID)
                    }
                }
            ]
        )

@app.event("message")
def handle_message_events(event, logger):
    if event.get("subtype") is not None:
        return

    logger.info(event)

def send_join_request(requester_id, client):
    client.chat_postMessage(
        channel=requester_id,
        text=config.JOIN_CONFIRMATION_MESSAGE
    )

    client.chat_postMessage(
        channel=config.USER_ID,
        text=config.JOIN_REQUEST_NOTIFICATION_MESSAGE.format(requester_id=requester_id),
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": config.JOIN_REQUEST_NOTIFICATION_MESSAGE.format(requester_id=requester_id)
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": config.ACCEPT_REQUEST_BUTTON_TEXT,
                            "emoji": True
                        },
                        "style": config.ACCEPT_BUTTON_STYLE,
                        "value": requester_id,
                        "action_id": config.ACCEPT_ACTION_ID
                    }
                ]
            }
        ]
    )

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
