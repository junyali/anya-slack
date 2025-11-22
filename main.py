from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from dotenv import load_dotenv

import os

load_dotenv()

SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

app = App(token=SLACK_BOT_TOKEN)

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
