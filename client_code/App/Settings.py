from anvil.js.window import jQuery as jQ
from anvil.js.window import document
from anvil_extras.storage import indexed_db

class SettingsClass:
    def __init__(self):
        self.store = indexed_db.create_store('cheteme-user')
        settings = self.store.get('settings')
        self.settings = settings if settings else {
            'navigation':3,
            'text':2
            }
        self.apply()

    def get(self):
        return self.settings

    def apply(self):
        style = f"""
        :root {{
  --h1-size: {self.settings['text'] * 1.5}rem;
  --h2-size: {self.settings['text'] * 1.25}rem;
  --p-size: {self.settings['text']}rem;
  --nav-size: {self.settings['navigation']}rem;
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