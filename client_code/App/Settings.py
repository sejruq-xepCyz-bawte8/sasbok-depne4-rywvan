#Cheteme Settings
from anvil.js.window import jQuery as jQ
from anvil.js.window import document
from anvil_extras.storage import indexed_db

class SettingsClass:
    def __init__(self):
        self.store = indexed_db.create_store('cheteme-user')
        self.renders_store = indexed_db.create_store('cheteme-renders')
        settings = self.store.get('settings')
        self.settings = settings if settings and settings.get('line') else {
            'navigation':5,
            'text':2,
            'cover': 150,
            'line':1.1,
            'words':10,
            'font':'Adys'
            }

        if not 'font' in self.settings:
          self.settings['font'] = 'Adys'
        self.apply()

    def get(self):
        return self.settings

    def apply(self):
        if self.settings['font'] in FONTS:
          font = FONTS[self.settings['font']]
        else:
          font = 'Adys'
        style = f"""
        :root {{
    --h1-size: {self.settings['text'] * 1.2}rem;
    --h2-size: {self.settings['text'] * 1.1}rem;
    --p-size: {self.settings['text']}rem;
    --p-line: {self.settings['line']};
    --nav-size: {self.settings['navigation']}rem;
    --cover-size: {self.settings['cover']}px;
    --words-distance: {self.settings['words']}px;
    --reader-font: {font};
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
        self.renders_store.clear()





FONTS = {
  'Adys':'Adys',
  'Arial':"'Arial', sans-serif",
  'Calibri':"'Calibri', sans-serif",
  'Century Gothic':"'Century Gothic', sans-serif",
  'Courier':"'Courier New CYR', 'Courier New', monospace",
  'Tahoma':"'Tahoma', sans-serif",
  'Trebuchet':"'Trebuchet MS', sans-serif",
  'Times New Roman':"'Times New Roman', serif",
  'Verdana':"'Verdana', sans-serif"
}