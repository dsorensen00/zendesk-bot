import json
import requests


class ZendeskRequesterBot:
    API = ''
    username = ''
    password = ''
    phonyTicket = {}

    def __init__(self, username, password, baseAPI, ticket):
        self.username = username
        self.password = password
        self.API = baseAPI
        self.phonyTicket = ticket

    def createTicket(self):
        if self.phonyTicket is None:
            return
        else:
            requests.post(self.API + 'tickets.json', auth=(self.username, self.password), json=(json.dumps(self.phonyTicket)))
