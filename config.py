USER_ID = "U082PAFDDS5"
CHANNEL_ID = "C091BU30NGK"

# Similar to sharing a workflow through its link
# Running the workflow command will post a workflow-style button in the channel you ran it in (like #neighbourhood)
ENABLE_WORKFLOW_COMMAND = True

# Slack commands MUST be registered in your Slack App
# They must NOT conflict with existing registered commands
# Please don't register conflicting command names
# PLEASE!! - Every Workspace Admin in the Slack
JOIN_COMMAND = "/join-junyaverse"
WORKFLOW_COMMAND = "/wf-junyaverse"

# This is sent to you
JOIN_CONFIRMATION_MESSAGE = "your request to join has been sent! please DO NOT resend requests. i receive all of them :neocat_think:"
# This is what other people see
JOIN_REQUEST_NOTIFICATION_MESSAGE = "Haiii cutiee!!!\nHope your day is great today :33 <@{requester_id}> wants to join your channel!!"

WORKFLOW_TEXT = "Join <@{user_id}>'s personal channel! :3"

ACCEPT_REQUEST_BUTTON_TEXT = "Accept"
JOIN_REQUEST_BUTTON_TEXT = "join!"

INVITE_SUCCESS_MESSAGE = "✅ <@{requester_id}> has been invited to <#{channel_id}>"
INVITE_FAILURE_MESSAGE = "❌ Failed to invite <@{requester_id}> to <#{channel_id}>"

ACCEPT_BUTTON_STYLE = "primary"
JOIN_BUTTON_STYLE = "primary"

WORKFLOW_JOIN_ACTION_ID = "workflow-join-button"
ACCEPT_ACTION_ID = "joinrequest-accept"
