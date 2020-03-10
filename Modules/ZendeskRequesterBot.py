import json
import requests


class ZendeskRequesterBot:
    """Class that represents a Zendesk Requester that can Create new Zendesk Tickets"""

    API = ''
    username = ''
    password = ''

# Setting the initial values of username, password, and baseAPI
    def __init__(self, username, password, baseAPI):
        self.username = username
        self.password = password
        self.API = baseAPI

    def createTicket(self, ticket):
        """Creates a new ticket as a requestor, returns new ticket ID"""

        if ticket is None:
            return
        else:
            request = requests.post(self.API + 'tickets.json', auth=(self.username, self.password), json=(ticket))
            response = request.text
            ticketId = json.loads(response)['id']
            return ticketId
