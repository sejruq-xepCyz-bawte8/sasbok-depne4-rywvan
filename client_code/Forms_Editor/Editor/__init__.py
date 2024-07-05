from ._anvil_designer import EditorTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from anvil.js.window import jQuery as jQ
from anvil.js.window import Quill, JSON
from anvil_extras import non_blocking
from ...App import NAVIGATION, EDITOR, ASSETS
import json

class Editor(EditorTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    NAVIGATION.set(nav_bar='editor')

    self.open_form = NAVIGATION.nav_open_form
    self.deferred_change = None

  def form_show(self, **event):
    #elements by order exec
    self.info = jQ('#info')
    self.editor_nav_text = jQ('#editor .nav-text')
    self.quill = Quill('#quill', ASSETS.get('json/quill_options.json'))
    self.sidebar = jQ('.ql-toolbar')
    self.editor = jQ('#quill')
    #set quill
    self.quill.on('text-change', self.quill_change)
    content = json.loads(EDITOR.content)
    self.quill.setContents(content)
    
    #update visuals
    self.sidebar.toggle()
    self.info.text("Формат")
    self.editor_nav_text.text(f"{EDITOR.data['words']}д. {EDITOR.data['size']}kb")
    
  def quill_change(self, *event):
    self.editor_nav_text.removeClass('saved')
    non_blocking.cancel(self.deferred_change)
    self.deferred_change = non_blocking.defer(self.parse_changes, 2)
   
  def parse_changes(self):
    #calc words
    text:str = self.quill.getText()
    lines = text.splitlines()
    EDITOR.data['words'] = len(text.split())
    #delta
    EDITOR.content = JSON.stringify(self.quill.getContents())
    EDITOR.data['size'] = int(len(EDITOR.content.encode('utf-8')) / 1024) #bytes->kb
    
    #saving
    EDITOR.save_work()
    #display info
    self.editor_nav_text.addClass('saved')
    self.editor_nav_text.text(f"{EDITOR.data['words']}д. {EDITOR.data['size']}kb")

    if EDITOR.data['size'] > 1_111_111:
      Notification('Надвишихте 1Мб размер на творбата', style='danger').show()
    elif EDITOR.data['size'] > 5_111_111:
      Notification('Надвишихте 5Мб размер на творбата', style='danger').show()
    

  def form_hide(self, **event_args):
    EDITOR.save_work()

  def sidebar_toggle(self, sender, **event):
    self.sidebar.toggle()


