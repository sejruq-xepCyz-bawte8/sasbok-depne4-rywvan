from ._anvil_designer import ReaderTemplate
from anvil import *
from ...App import NAVIGATION, API, READER, WORKS
from anvil.js.window import document
from anvil.js.window import jQuery as jQ
from anvil_extras import non_blocking
from time import time, sleep
import re

class Reader(ReaderTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    NAVIGATION.set(nav_bar='reader')

    self.open_form = NAVIGATION.nav_open_form

    self.open_time = time()

    self.bookmark = READER.get_bookmark(READER.current_id)

    self.time_reading = 0.0 if not self.bookmark else self.bookmark['time_reading']
    self.readed_pages = False if not self.bookmark else self.bookmark['readed_pages']
    self.readed = False if not self.bookmark else self.bookmark['readed']
    
    self.min_time = 1 + READER.data['words'] / 100
    
  
    
    

  def form_show(self, **event):
    back = jQ('#today')
    back.attr('id', READER.get_back())

    self.bookmark_icon = jQ('#bookmark')
    if self.bookmark:
       self.bookmark_icon.addClass('active')

    self.scroling_pages_info = None
    self.source = document.createElement("div")
    self.source.innerHTML = READER.content

    
    self.reader =  document.getElementById("cheteme_reader")
    self.targetHeigth = self.reader.offsetHeight
    #self.imagesHeigth:int = int(self.targetHeigth / 3)

    #LABELS self.pagesLabel = self.add_label() #"#navl-ViewerW-ViewerW_Work"
    self.work_link = document.getElementById('reader')
    self.pagesLabel = self.work_link.querySelectorAll('.nav-text')[0]

    #self.add_label(text=self.form_name)
    self.last_scroll = time()
    self.mostVisible = 1
    self.pages = []
    self.toc = []
    self.currentPage = None
    self.currentParagraph = None
    self.pageNumber = 0
    self.headingsCount = 0
#self.add_event_handler('show', self.createNewPage) 
#self.targetHeigth = self.reader.offsetHeight
        


    #Sidebars
    self.sidebar_toc = jQ('#reader-sidebar-toc')
    self.sidebar_toc.toggle()
    self.sidebar_social = jQ('#reader-sidebar-social')
    self.sidebar_social.toggle()
    self.sidebar_cover = jQ('#reader-sidebar-cover')
    self.sidebar_cover.toggle()


    #build panels
    toc = non_blocking.defer(self.build_toc, 0)
    social = non_blocking.defer(self.build_social, 0)
    cover = non_blocking.defer(self.build_cover, 0)


    #START PAGINATION


    if READER.data['words'] > 300:
       jQ('.fa-book-open').addClass('fa-beat')
       Notification("Приготвяне на страниците", style='info', timeout=0.1).show()
       sleep(0.1)

       self.distribute()
       jQ('.fa-book-open').removeClass('fa-beat')
    else:
       self.distribute()


    
    
    
  def distribute(self):
        sleep(0.1)
        self.targetHeigth = self.reader.offsetHeight
        #self.imagesHeigth:int = int(self.targetHeigth / 3)
        self.reader.innerHTML = ''
        #self.last_scroll = time()
        self.pages = []
        self.currentPage = None
        self.currentParagraph = None
        self.pageNumber = 0
        
        specials_pattern = r'<img[^>]*>|<a[^>]*>.*?</a>'

        self.createNewPage()
        for element in self.source.childNodes:
            if 'tagName' in element:
                if element.tagName.lower() == 'p':
                    
                    chunks = re.split(f'({specials_pattern})', element.innerHTML)
                    #words = element.innerHTML.split(' ')
                    self.createNewParagraph(element)
                    
                    #words = element.innerHTML.split(' ')
                    for chunk in chunks:
                        if len(chunk) == 0:
                          continue
                        if not chunk.startswith('<img') and not chunk.startswith('<a '):
                         
                          words = chunk.split(' ')
                          for word in words:
                            if len(word) == 0:
                               continue
                            span = document.createElement('span')
                            span.innerHTML = word
                            self.currentParagraph.appendChild(span)

                            if self.currentPage.offsetHeight > self.targetHeigth:
                              self.currentParagraph.removeChild(span)
                              self.createNewPage()
                              self.createNewParagraph(element)
                              self.currentParagraph.appendChild(span)
                        else:
                           
                           container = document.createElement('div')
                           container.innerHTML = chunk
                           special = container.firstChild

                           self.currentParagraph.appendChild(special)

                           if self.currentPage.offsetHeight > self.targetHeigth:
                              self.currentParagraph.removeChild(special)
                              self.createNewPage()
                              self.createNewParagraph(element)
                              self.currentParagraph.appendChild(special)
                           

                
                elif element.tagName.lower() == 'h1' and self.headingsCount > 0:
                    self.headingsCount += 1
                    self.createNewPage()
                    clone = element.cloneNode('true')
                    self.currentPage.appendChild(clone)
                    self.toc.append({'h':1, 'text':element.textContent, 'page':self.pageNumber})
                
                
                else:
                    if element.tagName.lower() == 'h1' :
                        self.headingsCount += 1
                        self.toc.append({'h':1, 'text':element.textContent, 'page':self.pageNumber})
                    clone = element.cloneNode('true')
                    self.currentPage.appendChild(clone)
                    if self.currentPage.offsetHeight > self.targetHeigth:
                        self.currentPage.removeChild(clone)
                        self.createNewPage()
                        self.currentPage.appendChild(clone)
                    if element.tagName.lower() == 'h2' :
                        self.toc.append({'h':2, 'text':element.textContent, 'page':self.pageNumber})
  
  def createNewPage(self):
        
        self.pageNumber += 1
        page = document.createElement('div')
        page.className = 'page'
        page.id = self.pageNumber
        self.currentPage = page
        self.pages.append(page)
        self.reader.appendChild(self.currentPage)
        self.pagesLabel.textContent = f"1/{self.pageNumber}"
        #self.goEnd.page = f"{self.pageNumber}"

  def createNewParagraph(self, sourceElement):
        self.currentParagraph = document.createElement('p')
        styleAttribute = sourceElement.getAttribute('style')
        if styleAttribute:
            self.currentParagraph.setAttribute('style', styleAttribute)
        css_classes = sourceElement.classList
        self.currentParagraph.classList.add(*css_classes)
        self.currentPage.appendChild(self.currentParagraph)

  def parse_most_visible(self):
      
      pages = document.querySelectorAll('.page')
      for page in pages:
          rect = page.getBoundingClientRect()
          id = page.id
          y = rect['y']
          if y < 30 and y > - 10:
              self.mostVisible = id
              break
              
      self.pagesLabel.textContent = f"{self.mostVisible}/{self.pageNumber}"
      self.check_readed()

  def check_readed(self):
      self.time_reading = time() - self.open_time
      if int(self.mostVisible) == int(self.pageNumber):
         self.readed_pages = True
      if self.time_reading > self.min_time and self.readed_pages:
         self.readed = True

            
  def scroll_reader(self, page, *event):
        non_blocking.cancel(self.scroling_pages_info)
        self.scroling_pages_info = non_blocking.defer(self.parse_most_visible, 0.2)
        if self.bookmark:
           READER.save_bookmark(page=self.mostVisible, time_reading=self.time_reading, readed=self.readed, readed_pages=self.readed_pages)


  def bookmark_click(self, sender, *event):
    READER.save_bookmark(page=self.mostVisible, time_reading=self.time_reading, readed=self.readed, readed_pages=self.readed_pages)
    self.bookmark_icon.toggleClass('active')
    if self.bookmark:
      READER.delete_bookmark(READER.current_id)
    

  def toc_click(self, sender, *event):
    self.sidebar_social.hide()
    self.sidebar_cover.hide()
    self.sidebar_toc.toggle()


  def social_click(self, sender, *event):
    self.check_readed()
    self.sidebar_toc.hide()
    self.sidebar_cover.hide()
    self.sidebar_social.toggle()
    if self.readed:
       self.tb_comment.enabled = True
       self.tb_comment.placeholder = 'коментар...'
       self.engage_comment.enabled = True
       self.engage_liked.enabled = True

  def build_toc(self):
    for t in self.toc:
      link = Link()
      text = t['text'] if t['h'] == 1 else f"  {t['text']}"
      if len(text) > 20 : text = text[:19] + "+"
      pagen = str(t['page'])
      dots = '.' * (24 - len(text) - len(pagen))
      link.text = '{}{}{}'.format(text, dots, pagen)
      link.font = 'Courier New, monospace'
      link.page = t['page']
      link.add_event_handler('click', self.toc_h1_click)
      self.add_component(link, slot='toc')

    self.add_component(Spacer(), slot='toc')
    words = Label(text=f"{READER.data['words']} думи")
    words.font = 'Courier New, monospace'
    self.add_component(words, slot='toc')


  def toc_h1_click(self, **event):
    sender = event['sender']
    document.getElementById(sender.page).scrollIntoView({ 'behavior': 'smooth', 'block': 'start' })



  def build_social(self):
    social = READER.get_work_social(READER.current_id)
    if social:
      for comment in social['comments']:
        label = Label(text=comment)
        self.add_component(label, slot='social-comments')
      self.l_likes.text = social.get('liked')
      self.tb_comment.text = social.get('me')
      if social.get('me_liked'):
         self.engage_liked.icon = "fa:heart"



  def engage(self, engage:str=None, **event):
     if event['sender'] == self.engage_liked:
        engage = 'engage_liked'
     elif event['sender'] == self.engage_comment:
        engage = 'engage_comment'
  
     data = {
        'genre':READER.data['genres'][2],
        'comment':self.tb_comment.text,
        'author_id': READER.data['author_id'],
        'age': READER.data['age']
     }
     eresult, success = API.request(api=engage, info=READER.current_id, data=data)
     

     if success == 200 and engage == 'engage_liked':
        self.engage_liked.icon = "fa:heart"
     elif success == 200 and engage == 'engage_comment':
        self.engage_comment.icon = "fa:comment"



  def build_cover(self):
    data_work = READER.data
    data_uri = data_work['uri']
    author_id = data_work['author_id']
    data_author = READER.get_work_data(author_id)


    jQ('#reader-cover-image').html(WORKS.make_cover(data_work))
    jQ('#reader-cover-genres').text(data_work['genres'])
    jQ('#reader-cover-description').text(data_work['descr'])
   
    if data_author:
       jQ('#reader-cover-author').text(data_author['title'])
       jQ('#reader-cover-author-description').text(data_author['descr'])
       #jQ('#reader-cover-author-genres').text(data_author['genres'])
       
       
       author_uri = data_author['uri']
       work_url = f'https://chete.me/{author_uri}/{data_uri}'
       
       jQ('reader-cover-url').attr('href', work_url).text(work_url)
       print(work_url)

  
  def cover_click(self, sender, *event):
    self.sidebar_toc.hide()
    self.sidebar_social.hide()
    self.sidebar_cover.toggle()



    
  def open_work(self, sender, *event):
     pass