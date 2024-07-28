#Cheteme Assets
import anvil.http
from anvil_extras.storage import indexed_db
from time import time, sleep


class AssetsClass:
    def __init__(self, origin, version):
        self.origin:str = origin
        self.assets:dict = {}
        self.store = indexed_db.create_store('cheteme-assets')
        self.version = version
        old_version = self.store.get('assets-version')
        if not old_version or old_version != self.version:
          self.store.clear()
          while len(self.store) != 0:
            sleep(0.1)
          self.store['assets-version'] = self.version
          
        elif not old_version:
          self.store['assets-version'] = self.version
          

    def fetch(self, file_path:str):
        is_json = True if file_path.endswith('.json') else False
        #url = f'{self.origin}_/theme/{file_path}'
        if self.origin == "chete.me":
          url = f'https://chete.me/_/theme/{file_path}'
        else:
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
        if asset:
          return asset
        
        asset = self.store.get(file_path)
        if asset:
          self.assets[file_path] = asset
          return asset
          
        asset = self.fetch(file_path=file_path)

        if asset:
          self.store[file_path] = asset
          self.assets[file_path] = asset
          return asset
        else:
          return None


    

    