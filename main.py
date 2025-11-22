from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from dotenv import load_dotenv

import os
import config

load_dotenv('tokens.env')

SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

app = App(token=SLACK_BOT_TOKEN)

@app.command("/join-junyaverse")
def handle_join_request(ack, command, client):
    ack()

    requester_id = command["user_id"]

    client.chat_postMessage(
        channel=requester_id,
        text="your request to join has been sent! please DO NOT resend requests. i receive all of them :neocat_think:"
    )

    client.chat_postMessage(
        channel=config.USER_ID,
        text=f"Haiii cutiee!!!\nHope your day is great today :33 <@{requester_id}> wants to join your channel!!",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Haiii cutiee!!!\nHope your day is great today :33 <@{requester_id}> wants to join your channel!!"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Accept",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": requester_id,
                        "action_id": "joinrequest-accept"
                    }
                ]
            }
        ]
    )

@app.action("joinrequest-accept")
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
            text=f"✅ <@{requester_id}> has been invited to <#{config.CHANNEL_ID}>",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"✅ <@{requester_id}> has been invited to <#{config.CHANNEL_ID}>"
                    }
                }
            ]
        )
    except Exception as e:
        client.chat_postMessage(
            channel=config.USER_ID,
            text=f"❌ Failed to invite <@{requester_id}> to <#{config.CHANNEL_ID}>",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"❌ Failed to invite <@{requester_id}> to <#{config.CHANNEL_ID}>"
                    }
                }
            ]
        )

@app.event("message")
def handle_message_events(event, logger):
    if event.get("subtype") is not None:
        return

    logger.info(event)

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
