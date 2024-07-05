import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from anvil.js.window import jQuery as jQ
from anvil.js.window import document
from anvil_extras.storage import indexed_db

class SettingsClass:
    def __init__(self):
        self.store = indexed_db.create_store('cheteme-user')
        settings = self.store.get('settings')
        self.settings = settings if settings and settings.get('line') else {
            'navigation':3,
            'text':2,
            'cover': 150,
            'line':1.1,
            'words':10,
            }
        self.apply()

    def get(self):
        return self.settings

    def apply(self):
        style = f"""
        :root {{
    --h1-size: {self.settings['text'] * 1.2}rem;
    --h2-size: {self.settings['text'] * 1.1}rem;
    --p-size: {self.settings['text']}rem;
    --p-line: {self.settings['line']};
    --nav-size: {self.settings['navigation']}rem;
    --cover-size: {self.settings['cover']}px;
    --words-distance: {self.settings['words']}px;
}}
"""
        element = document.getElementById('user-settings')
        if element:
            element.innerHTML = style
        else:
            element = document.createElement('style')
            element.id = 'user-settings'
            element.innerHTML = style
            document.head.appendChild(element)


    def set(self, data):
        self.store['settings'] = data
        self.settings = data
        self.apply()