import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
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
    
    