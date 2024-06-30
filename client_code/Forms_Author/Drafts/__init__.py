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

    self.all_work_ids = EDITOR.all_work_ids

  def form_show(self, **event):
    self.drafts_panel = jQ('#editor-drafts')
    self.parse_works()

  def parse_works(self):
    self.drafts_panel.html('')
    for work_id in EDITOR.all_work_ids:
      work = EDITOR.get_work(work_id=work_id)
      data = work['data']
      cover = WORKS.make_cover(data)
      self.drafts_panel.append(cover)


  def b_editor_click(self, **event):
    EDITOR.set_new_work()
    open_form('Forms_Editor.Editor')


  def open_work(self, sender, **event):
    work_id = sender.attr('id')
    if not self.delete_choise.checked:
      EDITOR.set_current_id(work_id)
      open_form('Forms_Editor.Editor')
    else:
      EDITOR.del_work(work_id=work_id)
      self.parse_works()
      self.delete_choise.checked = False



