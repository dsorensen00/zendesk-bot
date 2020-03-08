import Modules
import dotenv
import os

# Loading .env from root directory, setting username, password, and baseAPI
dotenv.load()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
baseAPI = os.getenv("BASE_API")

# Initializing both Agent and Requester with username, password, and baseAPI
zendeskAgent = Modules.ZendeskAgentBot(username, password, baseAPI)
zendeskRequester = Modules.ZendeskRequesterBot(username, password, baseAPI, "ticket")

zendeskAgent.getOpenTickets()
print(zendeskAgent.openTickets[0])