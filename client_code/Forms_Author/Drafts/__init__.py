from ._anvil_designer import DraftsTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, EDITOR, WORKS

class Drafts(DraftsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    NAVIGATION.set(nav_bar='author')
    self.open_form = NAVIGATION.nav_open_form

  def form_show(self, **event):
    self.drafts_panel = jQ('#drafts-panel')
    self.parse_works()

  def parse_works(self):
    self.drafts_panel.html('')
    for work_id in EDITOR.get_draft_ids():
      data = EDITOR.get_work_data(work_id=work_id)
      if data:
        cover = WORKS.make_cover(work_data=data)
        self.drafts_panel.append(cover)


  def b_new_work_click(self, **event):
    new = EDITOR.set_new_work()
    if new:
      open_form('Forms_Editor.Editor')

  def b_profile_click(self, **event):
    new = EDITOR.set_profile_work()
    if new:
      open_form('Forms_Editor.Editor')


  def open_work(self, sender, **event):
    if not self.delete_choise.checked:
      current = EDITOR.set_current(work_id=sender.attr('id'))
      if current:
        open_form('Forms_Editor.Editor')
    else:
      EDITOR.del_work(work_id=sender.attr('id'))
      self.parse_works()
      self.delete_choise.checked = False



