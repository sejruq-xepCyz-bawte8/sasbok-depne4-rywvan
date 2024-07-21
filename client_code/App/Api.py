import anvil.http
import json
from ..Helpers import hash_args
from anvil_extras.storage import indexed_db
from time import sleep, time



NO_CACHE_APIS = ['new_user', 'author_uri', 'publish_work', 'merge_users_ticket', 'merge_users', 'engage_ostay', 'engage_readed', 'engage_liked', 'engage_comment']

#together with info if is
REDO = ['get_last', 'get_work_social', 'get_authors', 'get_chart', 'get_work_data', 'get_work_content', 'get_home']

CACHE = ['get_last', 'get_chart', 'get_work_data', 'get_home'] #, 'get_work_social'



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
            sleep(0.1)
            response, status = self.http_request(api=api, info=info, data=data)
        if status != 200 and api in REDO:
            sleep(0.1)
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
        
        if api == 'get_work_data':
            url = f'{self.origin}/wd-{info}'
        elif api == 'get_work_content':
            url = f'{self.origin}/wc-{info}'
        elif api == 'get_last': #https://get-last.chete.me/
            url = f'{self.origin}/chart_last_age_{self.age}'
        elif api == 'get_chart':
            url = f'{self.origin}/chart_{info}_age_{self.age}'
        elif api == 'get_home': #separate
            url = f'{self.origin}/chart_home_age_{self.age}'
        elif api == 'get_authors':
            url = f'{self.origin}/list-authors-age-{self.age}'
        else:
            url = f'{self.origin}/ch'

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
                    
            