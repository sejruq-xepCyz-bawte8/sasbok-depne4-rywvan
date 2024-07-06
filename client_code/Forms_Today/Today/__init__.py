from ._anvil_designer import TodayTemplate
from anvil import *
from ...App import NAVIGATION, READER
from ...Covers_Builder import fill_panel


class Today(TodayTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)

    self.open_form = NAVIGATION.nav_open_form

    #self.work_template:str = ASSETS.get('html/work_cover.html') 
    

  def form_show(self, **event):
    fill_panel(panel_id='published', works=READER.get_last())
    fill_panel(panel_id='readed', works=READER.get_last())
    fill_panel(panel_id='liked', works=READER.get_last())



  def b_work_click(self, **event):
      open_form('Forms_Reader.Reader')


  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')