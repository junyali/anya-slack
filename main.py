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
    trigger_id = command["trigger_id"]
    send_join_request(requester_id, client, trigger_id=trigger_id)

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
        trigger_id = body["trigger_id"]
        send_join_request(requester_id, client, trigger_id=trigger_id)

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

@app.view("join_modal_submit")
def handle_modal_submission(ack, body, client, view):
    ack()

    requester_id = view["private_metadata"]
    responses = extract_modal_responses(view)

    send_join_request(requester_id, client, responses=responses)

@app.event("message")
def handle_message_events(event, logger):
    if event.get("subtype") is not None:
        return

    logger.info(event)

def send_join_request(requester_id, client, trigger_id=None, responses=None):
    if config.ENABLE_JOIN_MODAL and responses is None:
        if trigger_id:
            client.views_open(
                trigger_id=trigger_id,
                view={
                    "type": "modal",
                    "callback_id": "join_modal_submit",
                    "title": {
                        "type": "plain_text",
                        "text": "Questions"
                    },
                    "submit": {
                        "type": "plain_text",
                        "text": "Submit"
                    },
                    "blocks": build_modal_blocks(),
                    "private_metadata": requester_id
                }
            )
        return

    notification_text = config.JOIN_REQUEST_NOTIFICATION_MESSAGE.format(requester_id=requester_id)
    if responses:
        notification_text += format_responses_text(responses)

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
                    "text": notification_text
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

def build_modal_blocks():
    blocks = []
    for index, question in enumerate(config.JOIN_QUESTIONS):
        block = {
            "type": "input",
            "block_id": f"question_{index}",
            "label": {
                "type": "plain_text",
                "text": question["label"],
                "emoji": True
            },
            "element": {
                "type": "plain_text_input",
                "action_id": "answer",
                "multiline": question.get("multiline", False),
                "placeholder": {
                    "type": "plain_text",
                    "text": question.get("placeholder", "")
                }
            },
            "optional": question.get("optional", False)
        }
        blocks.append(block)

    return blocks

def extract_modal_responses(view):
    responses = []
    values = view["state"]["values"]

    for index, question in enumerate(config.JOIN_QUESTIONS):
        block_id = f"question_{index}"
        answer = values[block_id]["answer"]["value"]

        if answer:
            responses.append({
                "question": question["label"],
                "answer": answer
            })

    return responses

def format_responses_text(responses):
    if not responses:
        return ""

    text = "\n\n*Responses:*"
    for response in responses:
        answer = response["answer"].replace("\n", "\n  ")
        text += f"\n- {response['question']}\n  {answer}"

    return text

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
