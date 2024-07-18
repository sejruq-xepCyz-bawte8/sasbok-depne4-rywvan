import anvil.server
import anvil.http
from anvil.tables import app_tables
import json

        

@anvil.server.callable
def get_home_chart(age):
  row = app_tables.charts.get(api='get_home', age=age)
  return row


@anvil.server.background_task
def make_today_request():
  response = request_home(1)
  if response:
    save_chat(1, response)
  else:
    print('no resp 1')
    
  response = request_home(0)
  if response:
    save_chat(0, response)
  else:
    print('no resp 0')


def save_chat(age, response):
    row = app_tables.charts.get(api='get_home', age=age)
    if row:
      row['response'] = response
    else:
      app_tables.charts.add_row(age=age, api='get_home', response=response)

        
def request_home(age):
        headers:dict = {
        'Cheteme':'get_home',
        'Cheteme-Age':age
    }
        url = f'https://chete.me/api/chart-home-age-{age}'

        try:
                response = anvil.http.request(
                                        url=url,
                                        headers = headers,
                                        method='GET',
                                        json=True
                                        )
                status = 200
        except anvil.http.HttpError as e:
                response = None
                status = e.status
        return response
    
       
