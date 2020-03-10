import requests
import discord
from discord import Webhook, RequestsWebhookAdapter


class DiscordNotificationBot:
    """A bot that allows you to post notifications to specific webhooks"""

    webhook = None

    def __init__(self, webhookId, webhookToken):
        self.webhook = Webhook.partial(webhookId, webhookToken, adapter=RequestsWebhookAdapter())

    def postNotification(self, message):
        """Posts a message to a specified webhook"""
        if self.webhook != None:
            self.webhook.send(message)
        else:
            return