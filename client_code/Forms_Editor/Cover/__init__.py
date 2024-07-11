from ._anvil_designer import CoverTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from ...App import NAVIGATION, EDITOR, ASSETS, WORKS
from .Contrast import adjust_color_for_contrast
from .ImageCover import parse_cover_image

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
    self.mask.value = EDITOR.data['m_opacity']
    

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
      font_html = font.format(font=f, text=f)
      self.sidebar.append(font_html)


  def title_change(self, sender, **event_args):
    EDITOR.data['title'] = self.title.text()
    self.editor_nav_text.text(EDITOR.data['title'][0:10])
   
    

  def chose_font(self, sender, **event_args):
    EDITOR.data['font'] = sender.attr('font_cover')
    self.paint_cover()

  def chose_color(self, sender, **event_args):

    id = sender.attr('id')
    if id == 'color':
      color = sender.val()
      bg_color = EDITOR.data['bg_color']
      m_color = EDITOR.data['m_color']
      m_color = adjust_color_for_contrast(base_color=color, second_color=m_color, target_contrast=100)
      bg_color = adjust_color_for_contrast(base_color=color, second_color=bg_color, target_contrast=11)
    else:
      color = EDITOR.data['color']
      bg_color = sender.val()
      color = adjust_color_for_contrast(base_color=bg_color, second_color=color, target_contrast=11)
      m_color = EDITOR.data['m_color']
      m_color = adjust_color_for_contrast(base_color=color, second_color=m_color, target_contrast=100)

    EDITOR.data['color'] = color
    EDITOR.data['bg_color'] = bg_color
    EDITOR.data['m_color'] = m_color

    self.paint_cover()
    self.color.val(EDITOR.data['color'])
    self.bg_color.val(EDITOR.data['bg_color'])

  def form_hide(self, **event_args):
    EDITOR.save_work()

  def save_buffer(self):
    EDITOR.save_work()
    self.info.addClass('saved')
  
  def sidebar_toggle(self, sender, **event):
    sender.toggleClass('active')
    self.sidebar.toggle()

  def copy_permalink_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass


  def open_work(self, sender, **event):
    pass

  def file_loader_change(self, file, **event_args):
    image = parse_cover_image(file)
    if image:
      EDITOR.data['image'] = image
      self.paint_cover()
      EDITOR.save_work()
   

  def file_clean_click(self, **event_args):
    EDITOR.data['image'] = 0
    self.paint_cover()
    EDITOR.save_work()

  def mask_change(self, handle, **event_args):
    EDITOR.data['m_opacity'] = self.mask.value
    self.paint_cover()
    EDITOR.save_work()
