from ._anvil_designer import SearchTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, READER, API
from ...Covers_Builder import fill_panel



class Search(SearchTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.filters:set = set()
    self.chart:list = []
    self.open_form = NAVIGATION.nav_open_form

    READER.set_back("search")

  def form_show(self, **event):
    self.chart_panel = jQ('#charts-panel')
    self.chart_panel.text('+/- за И/Не; за автор -->')

  def b_search_click(self, sender, **event):
    search = self.search_for.text
    is_author = 1 if self.switch_1.checked else 0
    self.chart_panel.html('')
    if search != '':
      data = {
            'search':search,
            'is_author':is_author
        }
      found_works, success = API.request(api='search', data=data)
      if found_works and success:
        fill_panel(panel_id='charts-panel', works=found_works)
      else:
        self.chart_panel.text('няма намерени резултати')


  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')

    
