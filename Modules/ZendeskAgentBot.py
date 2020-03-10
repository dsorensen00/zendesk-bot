import requests
import json


class ZendeskAgentBot:
    """Class that represents a Zendesk Agent that can Update, and Get all Zendesk Tickets"""

    baseAPI = ''
    newTickets = []
    openTickets = []
    solvedTickets = []
    username = ''
    password = ''

# Setting the initial values of username, password, and baseAPI
    def __init__(self, username, password, baseAPI):
        self.username = username
        self.password = password
        self.baseAPI = baseAPI

    def getNewTickets(self):
        """Gets all NEW Zendesk Tickets, sets them to an array in ZendeskAgentBot.newTickets"""

        request = requests.get(self.baseAPI + 'search.json?query=type:ticket status:new', auth=(self.username, self.password))
        response = request.text
        tickets = json.loads(response)['results'] if json.loads(response)['count'] != 0 else None
        if tickets != None:
            for ticket in tickets:
                if ticket is None:
                    continue
                else:
                    self.newTickets.append(ticket)
                pass
        else:
            print('No New Tickets')

    def getOpenTickets(self):
        """Gets all OPEN Zendesk Tickets, sets them to an array in ZendeskAgentBot.openTickets"""

        request = requests.get(self.baseAPI + 'search.json?query=type:ticket status:open', auth=(self.username, self.password))
        response = request.text
        tickets = json.loads(response)['results'] if json.loads(response)['count'] != 0 else None
        if tickets != None:
            for ticket in tickets:
                if ticket is None:
                    continue
                else:
                    self.openTickets.append(ticket)
                pass
        else:
            print('No Open Tickets')

    def getSolvedTickets(self):
        """Gets all SOLVED Zendesk Tickets, sets them to an array in ZendeskAgentBot.solvedTickets"""

        request = requests.get(self.baseAPI + 'search.json?query=type:ticket status:open', auth=(self.username, self.password))
        response = request.text
        tickets = json.loads(response)['results'] if json.loads(response)['count'] != 0 else None
        if tickets != None:
            for ticket in tickets:
                if ticket is None:
                    continue
                else:
                    self.solvedTickets.append(ticket)
                pass
        else:
            print('No Solved Tickets')

    def updateTicket(self, ticketId, ticket):
        """Gets and updates specific ticket. Ticket is specified by ticket id"""

        request = requests.put(self.baseAPI + "tickets/" + str(ticketId) + '.json', auth=(self.username, self.password), json=(ticket))
        return request.status_code