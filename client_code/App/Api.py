import anvil.http
import json
from ..Helpers import hash_args
from anvil_extras.storage import indexed_db
from time import sleep, time



NO_CACHE_APIS = ['new_user', 'author_uri', 'publish_work', 'merge_users_ticket', 'merge_users', 'engage_ostay', 'engage_readed', 'engage_liked', 'engage_comment']

#together with info if is
#CACHE_LISTS = ['get_last', 'get_work_social', 'get_authors', 'get_chart']
#CACHE_WORKS = ['get_work_data', 'get_work_content', 'get_work_social']
CACHED = ['get_last', 'get_work_social', 'get_authors', 'get_chart', 'get_work_data', 'get_work_content', 'get_work_social']

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
        #if not data and api and api in CACHE_APIS:
        if api and api in CACHED:
            response, status = self.check_cache(api=api, info=info)

        if response and status:
            return response, status

        response, status = self.http_request(api=api, info=info, data=data)

        #try again :)
        if not response and api and api in CACHED:
            sleep(1)
            response, status = self.http_request(api=api, info=info, data=data)
        if not response and api and api in CACHED:
            sleep(1)
            response, status = self.http_request(api=api, info=info, data=data)

        if response and status == 200 and api and api in CACHED:
            self.save_cache(api=api, info=info, response=response)



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
    
    

    
    def check_cache(self, api:str, info:str=None):
        #api+info <-> response at time
        #self.store

        cache_id = f'{api}_{info}' if info else api
        cache = self.store.get(cache_id)
        if not cache:
            return False, False
        else:
            response = cache.get('response')
            timestamp = cache.get('timestamp')
        
        if not response or not timestamp:
            return False, False
        
        delta = time() - timestamp

        if delta > 3600: #one hour
            del self.store[cache_id]
            return False, False
        else:
            return response, 200


    

    def save_cache(self, api:str, info:str, response):
        cache_id = f'{api}_{info}' if info else api

        cache = {
            'response':response,
            'timestamp':time()
        }

        self.store[cache_id] = cache

        cached_ids = list(self.store)
        if len(cached_ids) > 3:
            ids_to_delete = cached_ids[:-3]
            for id in ids_to_delete:
                del self.store[id]

        
        


    def http_request(self, api, info, data):
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

        return response, status