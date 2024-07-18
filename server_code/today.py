import anvil.server
import anvil.http
import json
        

@anvil.server.background_task
def make_today_request():
  response = request_home()
  print(response)
        
def request_home():
        headers:dict = {
        'Cheteme':'get_home',
    }
        url1 = f'https://api.chete.me/chart-home-age-1'
        url0 = f'https://api.chete.me/chart-home-age-0'
        try:
                response = anvil.http.request(
                                        url=url1,
                                        headers = headers,
                                        method='GET',
                                        json=True
                                        )
                status = 200
        except anvil.http.HttpError as e:
                response = None
                status = e.status
        return response
    
       
