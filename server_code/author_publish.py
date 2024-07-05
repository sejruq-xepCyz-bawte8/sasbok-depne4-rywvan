import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


from CfApi import request
"""
The anvil.server.context.client object tells you about that client, including its type
(one of "browser", "http", "email", "uplink", "client_uplink" or "background_task").

For browsers and HTTP addresses,
you can also find the IP address (client.ip), and a geographical location estimated from that IP (client.location).

client is None when executing in the browser, or when executing on an Uplink but not as part of a server function. (In this situation, this code is the client!)"""

@anvil.server.callable
def execute_ticket(ticket:str):
  print('execute_ticket')
  
  client = anvil.server.context.client
  ip = client.ip #192.168.65.1
  type = client.type #browser

  if type == "browser" and ip != "192.168.65.1":
    print("production")
  else:
    print("dev")
    url = 'http://192.168.0.101:8787'
    request(api='ticket', info=ticket, url=url)

  return client.ip 


@anvil.server.callable
def new_author(data:dict):
  pass