import anvil.http
import json
from ..Helpers import hash_args
from anvil_extras.storage import indexed_db



NO_CACHE_APIS = ['new_user', 'author_uri', 'publish_work', 'merge_users_ticket', 'merge_users', 'engage_ostay', 'engage_readed', 'engage_liked', 'engage_comment']

class ApiClass:
    def __init__(self, get_user, version, origin:str):
        self.origin = origin
        self.user = get_user
        self.store = indexed_db.create_store('cheteme-cache')
        self.version = str(version)

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
        response = None
        status = None
        if api and api not in NO_CACHE_APIS:
            response, status = self.check_cache(api=api, data=data, info=info)

        if response and status:
            return response, status

        headers = self.parse_headers(api=api, info=info)
        if data:
            headers['Content-Type'] = 'application/json'
            #payload = json.dumps(data) if data else ''
            payload = data
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
        else:
            try:
                response = anvil.http.request(
                                        url=self.origin,
                                        headers = headers,
                                        method='GET',
                                        json=True
                                        )
                status = 200
            except anvil.http.HttpError as e:
                response = None
                status = e.status
        
        

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
    
    

    
    def check_cache(self, api:str, data:dict=None, info:str=None):
        data = json.dumps(data) if data else ''
        info = info if info else ''
        self.origin
        version = self.version
        cache_id = f'{api}-{info}'
        #hash = hash_args(self.origin, version, api, info, data)
        #print(cache_id, data)
        return False, False
    

    def save_cache(self, api:str, data:dict=None, info:str=None):
        data = json.dumps(data) if data else ''
        info = info if info else ''
        self.origin
        version = self.version
        cache_id = f'{api}-{info}'
        #hash = hash_args(self.origin, version, api, info, data)
        #print(cache_id)
        