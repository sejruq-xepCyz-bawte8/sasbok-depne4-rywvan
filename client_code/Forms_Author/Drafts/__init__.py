from ._anvil_designer import DraftsTemplate
from anvil import *
from ...App import NAVIGATION

class Drafts(DraftsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    NAVIGATION.set(nav_bar='author')
    self.open_form = NAVIGATION.open_form

  def form_show(self, **event):
    pass

  def b_editor_click(self, **event):
    open_form('Forms_Editor.Editor')


