#Cheteme API
import anvil.http
import json

class ApiClass:
    def __init__(self, get_user, version, origin:str):
        self.origin = origin
        self.user = get_user
        self.version = str(version)

        user = self.user()
        self.age = user['age'] if user else '0'
        self.user_id = user['user_id']
        self.secret = user['secret']
        self.cache = {}

    def parse_headers(self, api:str, info=None):
        user = self.user()
        user_id = user['user_id'] if user else 'new_user'
        secret = user['secret'] if user else 'new_user'
        age = user['age'] if user else '0'


        if isinstance(info, str) and len(info) > 150:
            info = 'info'
            
        headers:dict = {
        'Cheteme':api,
        'Cheteme-User': user_id,
        'Cheteme-Secret': secret,
        'Cheteme-Age': age,
        'Cheteme-Info': info
    }
        
        return headers
        
    def request(self, api:str, data:dict=None, info:str=None):
        response, status = self.http_request(api=api, info=info, data=data)

        if isinstance(response, list):
            return response, status
        elif isinstance(response, dict):
            message = response.get('message')
            if message:
                return message, status
            else:
                return response, status
        else:
            return response, status
    

    def http_request(self, api, info, data):
        headers = self.parse_headers(api=api, info=info)
        url = f'{self.origin}/ch'

        if data:
            headers['Content-Type'] = 'application/json'
            payload = data
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
    


