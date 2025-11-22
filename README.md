# Anya (Slack)

A customisable Slack bot that I might. Completely unrelated to the repository with the same name that holds the code for my Discord bot.

This is designed to be easily forkable and customisable for your own App in your own workspace.

**⚠️ The App MUST be installed in your private channel or this WILL NOT work!**

## Features

- **Two ways** to request access to a private channel: Direct slash command (`/join-channelname`) or a shareable workflow-style button (`/wf-channelname`)
- **Optional question modal**: Collect information from users requesting to join - dog or cat infrastructure? I pick cat purrsonally :3
- **Customisable**: I've said that word like 4 times already, but you can change anything. Questions, join messages, request messages, you name it
- **Socket Mode**: Doesn't rely on HTTP requests (which might get blocked by your organisation's firewall). You'll need to either self-host this or if you're in the Hack Club Slack, use nest!
- **(Kind of) simple setup**: Just have a Slack Application ready and plop in bot and app tokens

## How it works

1. User runs `/join-channelname` or clicks a button from `/wf-channelname`
2. (Optional) a modal pops up asking questions
3. User submits request to join
4. You receive a private DM from the app with the collected info and may wish to accept or ignore
5. Click accept and the app invites them to your private channel

![](./imgs/workflow.png)
![](./imgs/modal.png)
![](./imgs/msg.png)

## Setup

### Prerequisites

- Python 3.13 or higher (older versions may work, however this project was built and tested on 3.13)
- A Slack workspace where you have permission to install Apps
  - Workspace Admin is **NOT required**!

### Slack App

#### Creation

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and click **Create New App**
2. Choose **From scratch**
3. Give it a name (e.g., "Anya") and select your workspace
4. Click **Create App**

#### Permissions and Configuration

1. Enable **Socket Mode**
2. Generate a new App token and save it for later - it starts with 'xapp-'
3. Go to **OAuth & Permissions** and under **Bot Token Scopes**, give the Bot the following permissions:
   - `channels:manage`
   - `channels:read`
   - `chat:write`
   - `chat:write.customize`
   - `commands`
   - `groups:history`
   - `groups:read`
   - `groups:write`
   - `groups:write.invites`
   - `im:write`
   - `users:read`
   - `im:history`
4. Create slash commands
5. Install App to the workspace and copy the **Bot User OAuth token** - it starts with 'xoxb-'

### Installation

Clone this repository:
```bash
git clone https://github.com/junyali/anya-slack.git
cd anya-slack
```

Install dependencies:
```bash
pip install slack-bolt slack-sdk python-dotenv
```

Create a file called `tokens.env` in the project directory:
```env
SLACK_APP_TOKEN=xapp-your-app-level-token-here
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
```

Edit `config.py` with your settings:
```python
# Replace with your actual IDs
USER_ID = "U123456789"  # Your user ID
CHANNEL_ID = "C123456789"  # Your channel ID

# Customise your commands (must match what you created in Slack)
JOIN_COMMAND = "/join-channelname"
WORKFLOW_COMMAND = "/wf-channelname"

# Customise all messages, questions, etc.
# See the config.py file for all options
```

Run the bot:
```bash
python main.py
```

You should see `Bolt app is running!` if everything is set up correctly.

The bot needs to keep running for commands to work. If you close the terminal, the bot stops.
