import anvil.server
import anvil.http
import json
        
def parse_headers(api:str, info=None):
        #user = self.user()
        #user_id = user['user_id'] if user else 'new_user'
        #secret = user['secret'] if user else 'new_user'
        #age = user['age'] if user else '0'

        info = info if info and isinstance(info, str) and len(info) < 200 else ''
        headers:dict = {
        'Cheteme':api,
        'Cheteme-Anvil':'Cheteme-Anvil',
        'Cheteme-Info': info
    }
        return headers
        
def request(api:str, url:str, data:dict=None, info:str=None):
        headers = parse_headers(api=api, info=info)
        if data:
            payload = json.dumps(data) if data else ''
            try:
                response = anvil.http.request(
                                        url=url,
                                        headers = headers,
                                        method='POST',
                                        data=payload,
                                        json=True
                                        )
                status = 200
            except anvil.http.HttpError as e:
                response = None
                status = e.status
        else:
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
        return response, status
    
    
