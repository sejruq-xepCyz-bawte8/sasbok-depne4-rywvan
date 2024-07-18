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
    url = 'https://chete.me/api/'
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
    anvil_user_id = user.get('user_id')
    cheteme_user_id = data.get('user_id')

    #no author in that anvil user user case
    if not anvil_user_id and cheteme_user_id:
      user['author_id'] = data.get('author_id')
      user['user_id'] = data.get('user_id')
      data['is_registred'] = 1
      user['data'] = data

      message = {
        'new':True,
        'data':data
      }
      
      return message

    #is cheteme user in anvil user
    if anvil_user_id:
      message = {
        'new':False,
        'data':user['data']
      }
      return message
      