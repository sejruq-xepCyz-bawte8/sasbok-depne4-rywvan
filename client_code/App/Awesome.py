from anvil_extras.storage import indexed_db

class AwesomeClass:
    def __init__(self, fn_asset_get):
        self.icons = fn_asset_get('json/awesome.json')

    def get(self, bg:str, style:str='regular'):
        en = self.icons.get(bg)
        fa = f'fa-{style} fa-{en}' if en else ''
        return fa
    
    def get_4_anv(self, bg:str, style:str='regular'):
        en = self.icons.get(bg)
        fa = f'fa:{en}' if en else ''
        return fa
    
    