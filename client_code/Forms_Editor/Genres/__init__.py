from ._anvil_designer import GenresTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from anvil_extras.Chip import Chip
from ...App import NAVIGATION, EDITOR, ASSETS, AW

class Genres(GenresTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
  
    self.open_form = NAVIGATION.nav_open_form

    self.g_all = ASSETS.get('json/genres.json')
    self.g1 = self.g_all['g1']
    self.g2 = self.g_all['g2']

  def form_show(self, **event):
    self.info = jQ('#info')
    self.info.text('Икони')
    self.sidebar = jQ('#editor-option-sidebar')
    self.sidebar.toggle()


    keywords = ASSETS.get('json/awesome.json')
    self.buld_sidebar(keywords=keywords)
    self.keywords.suggestions = keywords


    genres = EDITOR.data['genres']
    pg1 = self.prep_genres()

    if genres[1]:
      self.genres_1.items = pg1 if genres[1] in pg1 else pg1 + [genres[1]]
      self.genres_1.selected_value = genres[1]
    else:
      self.genres_1.items = pg1
      if len(pg1) == 1 : self.genres_1.selected_value = pg1

    self.genres_2.items = self.g2
    if genres[2]:
      self.genres_2.selected_value = genres[2]
      g3s = self.g2[genres[2]]
    else:
      g3s = None
    
    if g3s:
      self.genres_3.enabled = True
      self.genres_3.items = g3s
    else:
      self.genres_3.enabled = False

    if genres[3] and g3s:
      self.genres_3.enabled = True
      self.genres_3.selected_value = genres[3]

    self.genres_1.border = '' if self.genres_1.selected_value else '1px solid LightSalmon'
    self.genres_2.border = '' if self.genres_2.selected_value else '1px solid LightSalmon'


  def prep_genres(self):
    
    words = EDITOR.data['words']

    if words <= 15:
      pg1 = ["микро разказ", "хайку", "стих"]

    elif words > 15 and words <= 40:
      pg1 = ["микро разказ", "стих"]

    elif words > 40 and words <= 100:
      pg1 = ["микро разказ", "стихотворение"]

    elif words > 100 and words <= 1000:
      pg1 = ["флашфикшън", "стихотворение"]

    elif words > 1000 and words <= 7500: #"разказ":{"wmin":1001, "wmax":7500},
      pg1 = ["разказ", "приказка"]

    elif words > 7500 and words <= 17500:
      pg1 = ["повест"]

    elif words > 17500 and words <= 40000:
      pg1 = ["новела"]

    else:
      pg1 = ["роман"]

    return pg1


  def buld_sidebar(self, keywords):
    
    icon = ASSETS.get('html/icon.html')
    for key, value in keywords.items():
      fa = AW.get(key)
      icon_html = icon.format(bg=key, fa=value)
      self.sidebar.append(icon_html)


  def form_hide(self, **event_args):
    EDITOR.save_work()

  
  def sidebar_toggle(self, sender, **event):
    self.sidebar.toggle()

  def keywords_change(self, sender, **event_args):
    EDITOR.data['keywords'].append(sender.text)
    EDITOR.save_work()
    chip = Chip()
    chip.add_event_handler('close_click', self.delete_keyword)
    self.fp_keywords.add_component(chip)

  def genres_1_change(self, sender, **event_args):
    g1 = self.genres_1.selected_value
    self.genres_1.border = '' if g1 else '1px solid LightSalmon'

    if g1:
      g0 = self.g1[g1]
      EDITOR.data['genres'][0] = g0
      EDITOR.data['genres'][1] = g1
      EDITOR.save_work()
   
  def genres_2_change(self, sender, **event_args):
    g2 = self.genres_2.selected_value
    self.genres_2.border = '' if g2 else '1px solid LightSalmon'
    if g2:
      EDITOR.data['genres'][2] = g2
      EDITOR.data['genres'][3] = None

      g3s = self.g2[g2]
      if g3s:
        self.genres_3.enabled = True
        self.genres_3.items = g3s
      else:
        self.genres_3.enabled = False
        self.genres_3.items = []

      EDITOR.save_work()





  def genres_3_change(self, sender, **event_args):
    g3 = self.genres_3.selected_value
    if g3:
      EDITOR.data['genres'][3] = g3
      EDITOR.save_work()