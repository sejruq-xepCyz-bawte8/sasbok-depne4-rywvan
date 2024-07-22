from ._anvil_designer import ChartsTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, READER, API, USER
from ...Covers_Builder import fill_panel
from datetime import datetime, timedelta

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

PERIODS:set = {'днес', 'седмицата', 'месеца'}

ENGAGEMENTS:set = {'харесани', 'публикувани', 'четени', 'коментирани'}


class Charts(ChartsTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.filters = READER.get_filters()
    self.chart:list = []
    self.open_form = NAVIGATION.nav_open_form
    READER.set_back("charts")


  def form_show(self, **event):
    
    #self.chart_name = jQ('#chart_name')
    self.filter_toggle(sender=None)
    #self.chart_name.text("Последни 100 публикувани ")



  def filter_toggle(self, sender, *event):
    filter = sender.attr('id') if sender else None
    if filter in self.filters:
      self.filters.remove(filter)
    else:
      if filter in PERIODS:
        self.filters.difference_update(PERIODS)
  
      if filter in ENGAGEMENTS:
        self.filters.difference_update(ENGAGEMENTS)
      
      self.filters.add(filter)

    jQ('.filter-fa').removeClass('fa-duotone')

    for filter in self.filters:
      jQ(f'#{filter}').find('.filter-fa').addClass('fa-duotone')
   
   
    READER.set_filters(self.filters)

    self.make_chart()



  def open_work(self, sender, **event):
    current = READER.set_current(sender.attr('id'))
    if current:
      open_form('Forms_Reader.Reader')


  def make_chart(self):

    if 'публикувани' in self.filters:
      self.chart, success = API.request(api=f'get_last')
      #self.chart = READER.get_last()
      if 'днес' in self.filters:
            self.chart = [c for c in self.chart if c['ptime'] > self.unix_today()]
      elif 'седмицата' in self.filters:
            self.chart = [c for c in self.chart if c['ptime'] > self.unix_week()]
      else:
            self.chart = [c for c in self.chart if c['ptime'] > 0]
      
      self.chart = sorted(self.chart, key=lambda x: x['ptime'], reverse=True)

    else:
      if 'днес' in self.filters:
            self.chart, success = API.request(api=f'get_chart', info = 'today')
      elif 'седмицата' in self.filters:
            self.chart, success = API.request(api=f'get_chart', info = 'week')
      else:
            self.chart, success = API.request(api=f'get_chart', info = 'month')

#elif 'харесани' in self.filters or 'четени' in self.filters or 'коментирани' in self.filters:
    
    genres =  GENRES & self.filters

    if genres:
      self.chart = [c for c in self.chart if c['g'] in genres]


    if 'харесани' in self.filters:
      self.chart = [c for c in self.chart if c['l'] > 0]
      self.chart = sorted(self.chart, key=lambda x: x['l'], reverse=True)
    elif 'четени' in self.filters:
      self.chart = [c for c in self.chart if c['r'] > 0]
      self.chart = sorted(self.chart, key=lambda x: x['r'], reverse=True)
    elif 'коментирани' in self.filters:
      self.chart = [c for c in self.chart if c['c'] > 0]
      self.chart = sorted(self.chart, key=lambda x: x['c'], reverse=True)
    
    
    fill_panel(panel_id='charts-panel', works=self.chart)


  def unix_today(self):
      now = datetime.now()
      beginning_of_today = datetime(now.year, now.month, now.day)
      return beginning_of_today.timestamp()
  


  def unix_week(self):  

    now = datetime.now()
    beginning_of_week = now - timedelta(days=now.weekday())
    beginning_of_week = datetime(beginning_of_week.year, beginning_of_week.month, beginning_of_week.day)
    return beginning_of_week.timestamp()