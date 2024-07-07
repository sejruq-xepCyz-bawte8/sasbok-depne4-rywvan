from ._anvil_designer import SearchTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, READER
from ...Covers_Builder import fill_panel

GENRES:set = {'фантастика',
'фентъзи',
'приключенски',
'ужаси',
'хумор',
'трилър',
'крими',
'драма',
'романс',
'детски',
'съвременни',
'действителни',
'исторически',
'еротика'}


class Search(SearchTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.filters:set = set()
    self.chart:list = []
    self.open_form = NAVIGATION.nav_open_form

    READER.set_back("search")

  def form_show(self, **event):
  
    self.chart_name = jQ('#chart_name')
    self.chart_panel = jQ('#charts-panel')
    self.chart_name.text("Последни 100 публикувани ")


  def b_search_click(self, sender, **event):
    search = self.search_for.text
    self.chart_panel.html('')
    fill_panel(panel_id='charts-panel', works=READER.search(search))
    

  def search_for_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass


  def clean_search_click(self, **event_args):
    self.search_for.text = ''
    self.clean_filters()
    

  def search_for_focus(self, **event_args):
    self.clean_filters()

  def clean_filters(self):
    self.filters.clear()
    jQ('.filter-fa').removeClass('fa-duotone')


  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')


    if 'публикувани' in self.filters:
      self.chart = READER.get_last()
    elif 'харесани' in self.filters or 'четени' in self.filters or 'коментирани' in self.filters:
          print('CHART')
          if 'днес' in self.filters:
            self.chart = READER.get_chart('today')
          elif 'седмицата' in self.filters:
            self.chart = READER.get_chart('week')
          else:
            self.chart = READER.get_chart('month')
    else:
      self.chart = READER.get_last()

    
    genres =  GENRES & self.filters
    print('genres', genres, self.filters, GENRES)
    print('bef', self.chart)

    if genres:
      self.chart = [c for c in self.chart if c['g'] in genres]
    

    print('af', self.chart)

    fill_panel(panel_id='charts-panel', works=self.chart)