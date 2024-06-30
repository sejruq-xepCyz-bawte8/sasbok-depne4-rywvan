from ._anvil_designer import EditorTemplate
from anvil import *
from ...App import NAVIGATION

class Editor(EditorTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    NAVIGATION.set(nav_bar='editor')
    self.open_form = NAVIGATION.open_form

  def form_show(self, **event):
    pass



