import anvil.http

class AssetsClass:
    def __init__(self, origin):
        self.origin:str = origin
        self.assets:dict = {}
        

    def fetch(self, file_path:str, json:bool):
        url = f'{self.origin}/_/theme/{file_path}'
        try:
            response = anvil.http.request(url=url,method='GET',json=json)
        except:
            response = None
        
        if json:
            return response
        elif response:
            response_bytes:bytes = response.get_bytes()
            response_string:str = response_bytes.decode('utf-8')
            return response_string
        else:
            return response

    def get(self, file_path:str):
        json = True if file_path.endswith('.json') else False
        asset = self.assets.get(file_path)
        if asset:
            return asset
        else:
            asset = self.fetch(file_path=file_path, json=json)
            self.assets[file_path] = asset
            return asset



