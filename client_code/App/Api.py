import anvil.http
import json


class ChetemeApi:
    def __init__(self, get_user, origin:str):
        self.origin = origin
        self.user = get_user
        

    def parse_headers(self, api:str, info=None):
        user = self.user()
        user_id = user['user_id'] if user else 'new_user'
        secret = user['secret'] if user else 'new_user'

        info = info if info and isinstance(info, str) and len(info) < 20 else 'info'
        headers:dict = {
        'Cheteme':api,
        'Cheteme-User': user_id,
        'Cheteme-Secret': secret,
        'Cheteme-Info': info
    }
        return headers
        
    def request(self, api:str, data:dict=None, info:str=None):
        headers = self.parse_headers(api=api, info=info)
        payload = json.dumps(data) if data else ''
        try:
            response = anvil.http.request(
                                    url=self.origin,
                                    headers = headers,
                                    method='POST',
                                    data=payload,
                                    json=True
                                    )
            status = 200
        except anvil.http.HttpError as e:
            response = None
            status = e.status
        
        return response, status