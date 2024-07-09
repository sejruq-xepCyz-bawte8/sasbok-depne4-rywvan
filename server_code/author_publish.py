import anvil.google.auth, anvil.google.drive, anvil.google.mail
import anvil.users
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
    url = 'https://chete.me'
    request(api='ticket', info=ticket, url=url)
  else:
    print("dev")
    url = 'http://192.168.0.101:8787'
    request(api='ticket', info=ticket, url=url)

  return client.ip 


@anvil.server.callable
def new_author(data:dict):
  pass


@anvil.server.callable
def parse_user_author(data:dict):
  user = anvil.users.get_user()
  if user:
    author_id = user.get('author_id')
    if not author_id and data['author_id']:
      user['author_id'] = author_id