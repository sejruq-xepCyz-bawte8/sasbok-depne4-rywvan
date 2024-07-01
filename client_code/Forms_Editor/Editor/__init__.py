from ._anvil_designer import EditorTemplate
from anvil import *
from anvil.js.window import jQuery as jQ
from anvil_extras import non_blocking
from ...App import NAVIGATION, EDITOR

class Editor(EditorTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)

    self.work = EDITOR.get_current_work()
    
    NAVIGATION.set(nav_bar='editor')
    self.open_form = NAVIGATION.nav_open_form


    toolbarOptions:list = [
      [{ 'header': 1 },
      { 'header': 2 },
      { 'align': 'center' },
      { 'align': 'right' },
      { 'list': 'bullet' },
        'blockquote',
        'bold',
        'italic',
        'image',
        'link',
        'clean'
      ],
    ]

    self.quill.toolbar=toolbarOptions
    self.quill.sanitize=False
    self.deferred_change = None
    self.deferred_save = None

  def form_show(self, **event):
    self.info = jQ('#info')
    self.sidebar = jQ('.ql-toolbar')
    self.sidebar.toggle()
    self.editor_nav_text = jQ('#editor .nav-text')
    self.info.text(f"{self.work['data']['words']}д. {self.work['data']['size']}kb")
    self.editor_nav_text.text(self.work['data']['title'][0:10])

    self.quill.set_html(self.work['html'], sanitize=False)

  def quill_change(self, **event):
    non_blocking.cancel(self.deferred_change)
    non_blocking.cancel(self.deferred_save)
    self.deferred_change = non_blocking.defer(self.changes_calc, 1)
    self.deferred_save = non_blocking.defer(self.save_buffer, 3)
    

  def sidebar_toggle(self, sender, **event):
    self.sidebar.toggle()

    
  def changes_calc(self):
    self.info.removeClass('saved')
    html = self.quill.get_html()
    text = self.quill.get_text()
    words = len(text.split())
    size = int(len(html.encode('utf-8')) / 1024) #bytes->kb
    
    self.work['data']['words'] = words
    self.work['data']['size'] = size
    self.work['html'] = html

    self.info.text(f"{self.work['data']['words']}д. {self.work['data']['size']}kb")
    
    if size > 1_111_111:
      
      Notification('Надвишихте 1Мб размер на творбата', style='danger').show()
    
    elif size > 5_111_111:
      
      Notification('Надвишихте 5Мб размер на творбата', style='danger').show()
    


  def form_hide(self, **event_args):
    self.save_buffer()

  def save_buffer(self):
    EDITOR.save_work(self.work)
    self.info.addClass('saved')
    
  def sidebar_toggle(self, sender, **event):
    self.sidebar.toggle()



