from ._anvil_designer import CoverTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, EDITOR, ASSETS, WORKS

class Cover(CoverTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    self.open_form = NAVIGATION.nav_open_form
    self.fonts = ASSETS.get('json/fonts.json')

  def form_show(self, **event):
    self.info = jQ('#info')
    self.info.text('Шрифтове')
    self.sidebar = jQ('#editor-option-sidebar')
    self.editor_nav_text = jQ('#editor .nav-text')
    self.sidebar.toggle()
    self.buld_sidebar()


    self.cover = jQ('#cover-container')

    self.color = jQ('#color')
    self.bg_color = jQ('#bg_color')



    self.color.val(EDITOR.data['color'])
    self.bg_color.val(EDITOR.data['bg_color'])

    

    self.paint_cover()


  def paint_cover(self):
    self.cover.html('')
    cover = WORKS.make_cover(EDITOR.data)
 
    self.cover.append(cover)
    self.title = jQ('.ch-work-title')
    self.title.attr('contenteditable', 'true')
    self.title.on('input', self.title_change)




  def buld_sidebar(self):
    font = ASSETS.get('html/font.html')
    for f in self.fonts:
      font_html = font.format(font=f, text="Заглавие")
      self.sidebar.append(font_html)


  def title_change(self, sender, **event_args):
    EDITOR.data['title'] = self.title.text()
    self.editor_nav_text.text(EDITOR.data['title'][0:10])
    print(EDITOR.data['title'])
    

  def chose_font(self, sender, **event_args):
    EDITOR.data['font'] = sender.attr('id')
    self.paint_cover()

  def chose_color(self, sender, **event_args):
    EDITOR.data[sender.attr('id')] = sender.val()
    self.paint_cover()

  def form_hide(self, **event_args):
    EDITOR.save_work()

  def save_buffer(self):
    EDITOR.save_work()
    self.info.addClass('saved')
  
  def sidebar_toggle(self, sender, **event):
    self.sidebar.toggle()

  def copy_permalink_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass


  def open_work(self, sender, **event):
    pass