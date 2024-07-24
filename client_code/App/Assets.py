import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.http
from anvil_extras.storage import indexed_db
from time import time


class AssetsClass:
    def __init__(self, origin, version):
        self.origin:str = origin
        self.assets:dict = {}
        self.store = indexed_db.create_store('cheteme-assets')
        self.version = version

    def fetch(self, file_path:str):
        is_json = True if file_path.endswith('.json') else False      
        url = f'{self.origin}/_/theme/{file_path}'
        if not self.origin:
          url = f'_/theme/{file_path}'
        try:
            response = anvil.http.request(url=url,method='GET',json=is_json)
        except:
            response = None
        
        if is_json:
            return response
        elif response:
            response_bytes:bytes = response.get_bytes()
            response_string:str = response_bytes.decode('utf-8')
            return response_string
        else:
            return response

    def get(self, file_path:str):
        asset = self.assets.get(file_path)
        if asset: return asset
        asset = self.get_cache(file_path)
        if asset: return asset
        asset = self.fetch(file_path=file_path)
        self.save_cache(file_path=file_path, response=asset)
        return asset

    def get_cache(self, file_path:str):
        asset = self.store.get(file_path)
        if asset:
            asset_version = asset['version']
            if asset_version == self.version:
                self.assets[file_path] = asset['response']
                return asset['response']
        return None
    
    def save_cache(self, file_path:str, response):
        self.store[file_path] = {
            'response':response,
            'version':self.version,
            'ctime':time()
        }
        self.assets[file_path] = response
    