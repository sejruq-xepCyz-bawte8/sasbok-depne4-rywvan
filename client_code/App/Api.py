import anvil.http
import json
from ..Helpers import hash_args
from anvil_extras.storage import indexed_db
from time import sleep, time



NO_CACHE_APIS = ['new_user', 'author_uri', 'publish_work', 'merge_users_ticket', 'merge_users', 'engage_ostay', 'engage_readed', 'engage_liked', 'engage_comment']

#together with info if is
REDO = ['get_last', 'get_work_social', 'get_authors', 'get_chart', 'get_work_data', 'get_work_content']

CACHE = ['get_last', 'get_chart', 'get_work_data'] #, 'get_work_social'

CACHED_DELTA = {'get_authors':1800,
                'get_work_content':1800,
                'get_work_social':5
                }

class ApiClass:
    def __init__(self, get_user, version, origin:str):
        self.origin = origin
        self.user = get_user
        self.store = indexed_db.create_store('cheteme-cache')
        self.store.clear()
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

        #try again :)
        if status != 200 and api in REDO:
            sleep(0.2)
            response, status = self.http_request(api=api, info=info, data=data)
        if status != 200 and api in REDO:
            sleep(0.5)
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
    
    

    
    def check_cache_(self, api:str, info:str=None):
        
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

        if delta > CACHED_DELTA[api]: #one hour 3600s
            del self.store[cache_id]
            return False, False
        else:
            
            return response, 200


    

    def save_cache_(self, api:str, info:str, response):
        cache_id = f'{api}_{info}' if info else api

        cache = {
            'response':response,
            'timestamp':time()
        }

        self.store[cache_id] = cache

        
        if len(self.store) > 5:
            cached_ids = list(self.store)
            ids_to_delete = cached_ids[50:] #[:-10] [5:]
            for id in ids_to_delete:
                del self.store[id]

        
    def delete_cashe_work_(self, work_id):
        cache_data_id = f'get_work_data_{work_id}'
        cache_content_id = f'get_work_content_{work_id}'
        if cache_data_id in self.store:
            del self.store[cache_data_id]
        if cache_content_id in self.store:
            del self.store[cache_content_id]


    def http_request(self, api, info, data):
        headers = self.parse_headers(api=api, info=info)
        
        if api == 'get_work_data':
            url = f'{self.origin}/wd-{info}'
        elif api == 'get_last': #https://get-last.chete.me/
            url = f'{self.origin}/chart-last-age-{self.age}'
        elif api == 'get_chart':
            url = f'{self.origin}/chart-{info}-age-{self.age}'
        elif api == 'get_today':
            url = f'{self.origin}/chart-today-age-{self.age}'
        else:
            url = self.origin

        if api in CACHE:
            response = self.fetch_cache(url=url)
            if response:
                return response, 200


        if data:
            headers['Content-Type'] = 'application/json'
            #payload = json.dumps(data) if data else ''
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

        if api in CACHE and status == 200:
            self.update_cache(url=url, response=response)

        return response, status
    

    def fetch_cache(self, url):

        cache = self.cache.get(url)
        
        if cache:
            timestamp = cache.get('timestamp')
            if time() - timestamp < 600:
                response = cache.get('response')
                if response:
                    return response
                else:
                    del self.cache[url]
            else:
                del self.cache[url]
        
        return None
    
    def update_cache(self, url, response):
        cache = {
            'response':response,
            'timestamp':time()
        }
        self.cache[url] = cache
                    
            