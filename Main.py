import Modules
import dotenv
import os
import datetime
from dateutil.parser import parse
import pytz
import time

# Loading .env from root directory and setting initial values
dotenv.load()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
baseAPI = os.getenv("BASE_API")
# Number of hours since last ticket update that will notify agent
notificationThreshold = os.getenv("NOTIFICATION_THRESHOLD")
discordWebhookId = os.getenv("DISCORD_WEBHOOK_ID")
discordWebhookToken = os.getenv("DISCORD_WEBHOOK_TOKEN")

# Initializing both Agent and Requester with username, password, and baseAPI
zendeskAgent = Modules.ZendeskAgentBot(username, password, baseAPI)
zendeskRequester = Modules.ZendeskRequesterBot(username, password, baseAPI)
# Initializing DiscordNotificationBot
discordNotification = Modules.DiscordNotificationBot(discordWebhookId, discordWebhookToken)

while True:
    notificationDate = datetime.datetime.now() - datetime.timedelta(hours=int(notificationThreshold))

# Get all open tickets, check to see if they have been updated within the notification threshold,
# if not updated within notification threshold, send discord notification
    zendeskAgent.getOpenTickets()
    for openTicket in zendeskAgent.openTickets:
        if openTicket['updated_at']:
            updated_at = parse(openTicket['updated_at'])
            if updated_at < pytz.utc.localize(notificationDate):
                discordNotification.postNotification("<@314621446808797204>, A user has been waiting longer than " + notificationThreshold+" hours for a response:\n\n"+"```\n" + openTicket['description'][:1800]+"\n```")

# Give Zendesk API a break, so we don't get banned for too many requests
    # time.sleep(60)

# Getting all new tickets, adding a new comment from agent, and marking as open
    zendeskAgent.getNewTickets()
    for newTicket in zendeskAgent.newTickets:
        if newTicket['id']:
            # TODO: make this a config/env value
            firstReplyTicketUpdate = {
                "ticket": {
                    "status": "open",
                    "comment":
                        {
                            "body": "Hey there chef!\n\nThank you for reaching out to Salad Support! Just wanted you to know that your support ticket has been received and that our support team will be reviewing it within the next 24 hours if a weekday, or by the next weekday if submitted on a weekend. In the meantime you can look over some of our support guides found at the link below, and see if you can't figure it out before hand, or head to our Discord channel (link also below). If you are having issues with GPU compatibility, please know that our engineers are hard at work trying to support all GPUs and in the meantime, we are unable to add more GPUs to our whitelist. Fortunately, you will still be able to earn through referring qualified friends and earn up to $2 for the first $4 each friend earns!\n\nSupport Guides: https://salad.zendesk.com/hc/en-us\n\nDiscord Channel: https://discord.gg/salad\n\nThanks again for reaching out, and one of our support staff should be going over your ticket and responding to you shortly.\n\n-Damon"
                        }
                }
            }
            zendeskAgent.updateTicket(newTicket['id'], firstReplyTicketUpdate)

# Give Zendesk API a break, so we don't get banned for too many requests
    # time.sleep(60)

# TODO: Make this a config/env array to randomly choose new requests
    phonyTicket = {
        "ticket": {
            "subject":   "Hello",
            "comment":   {"body": "Some question"},
            "requester": {"name": "Pablo", "email": "pablito@example.org"},
        }
    }
    phonyIds = []
# Creating couple new tickets, then resolving them to help with our first reply time
    for i in range(0, 3):
        id = zendeskRequester.createTicket(phonyTicket)
        if id != None:
            phonyIds.append(id)

# Give Zendesk API a break, so we don't get banned for too many requests
    # time.sleep(60)

# Now going to reply and solve all phony tickets
    for id in phonyIds:
        if id != None and id != 0:
            phonyTicketResponse = {
                "ticket": {
                    "status": "solved",
                    "subject": "Support Request Received",
                    "comment":
                        {
                            "body": "Hey there chef!\n\nThank you for reaching out to Salad Support! Just wanted you to know that your support ticket has been received and that our support team will be reviewing it within the next 24 hours if a weekday, or by the next weekday if submitted on a weekend. In the meantime you can look over some of our support guides found at the link below, and see if you can't figure it out before hand, or head to our Discord channel (link also below). If you are having issues with GPU compatibility, please know that our engineers are hard at work trying to support all GPUs and in the meantime, we are unable to add more GPUs to our whitelist. Fortunately, you will still be able to earn through referring qualified friends and earn up to $2 for the first $4 each friend earns!\n\nSupport Guides: https://salad.zendesk.com/hc/en-us\n\nDiscord Channel: https://discord.gg/salad\n\nThanks again for reaching out, and one of our support staff should be going over your ticket and responding to you shortly.\n\n-Damon"
                        }
                }
            }
            zendeskAgent.updateTicket(id, phonyTicketResponse)

# Now wait an hour to start the loop again
    time.sleep(3600)
