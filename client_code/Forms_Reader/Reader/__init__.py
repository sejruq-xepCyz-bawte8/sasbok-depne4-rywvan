from ._anvil_designer import ReaderTemplate
from anvil import *
from ...App import NAVIGATION, API, READER
from anvil.js.window import document
from anvil.js.window import jQuery as jQ
from anvil_extras import non_blocking
from time import time, sleep

class Reader(ReaderTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    
    NAVIGATION.set(nav_bar='reader')
    self.open_form = NAVIGATION.nav_open_form

    self.open_time = time()
    self.time_reading = 0.0
    self.readed_pages = False
    self.readed = False
    self.min_time = 1 + READER.data['words'] / 100
    
    

  def form_show(self, **event):

    self.scroling_pages_info = None
    self.source = document.createElement("div")
    self.source.innerHTML = READER.content
    #for node in self.source.childNodes:
    #    print(node)
    #App.READER CONTAINER 
    
    self.reader =  document.getElementById("cheteme_reader")
    self.reader.setAttribute('onscroll', 'anvil.call($("#appGoesHere > div"), "scroll_reader", $(this))')
    self.targetHeigth = self.reader.offsetHeight
    self.imagesHeigth:int = int(self.targetHeigth / 3)

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
        
    #START PAGINATION
    self.distribute()

    #Sidebars
    self.sidebar_toc = jQ('#reader-sidebar-toc')
    self.sidebar_toc.toggle()
    self.sidebar_social = jQ('#reader-sidebar-social')
    self.sidebar_social.toggle()

    self.build_toc()
    self.build_social()

    
    
  def distribute(self):
        self.reader.innerHTML = ''
        self.last_scroll = time()
        self.pages = []
        self.currentPage = None
        self.currentParagraph = None
        self.pageNumber = 0
        #self.add_event_handler('show', self.createNewPage)


        self.createNewPage()
        for element in self.source.childNodes:
            if 'tagName' in element:
                if element.tagName.lower() == 'p':
                    words = element.innerHTML.split(' ')
                    self.createNewParagraph(element)
                    for word in words:
                        if word.startswith('src="data:image'):
                          wordSpan = document.createElement('img')
                          wordSpan.src = word.split('"')[1]

                        else:
                          wordSpan = document.createElement('span')
                          wordSpan.innerHTML = word
                        
                        self.currentParagraph.appendChild(wordSpan)

                        if self.currentPage.offsetHeight > self.targetHeigth:
                          self.currentParagraph.removeChild(wordSpan)
                          self.createNewPage()
                          self.createNewParagraph(element)
                          self.currentParagraph.appendChild(wordSpan)
                
                elif element.tagName.lower() == 'h1' and self.headingsCount > 0:
                    self.headingsCount += 1
                    self.createNewPage()
                    clone = element.cloneNode('true')
                    self.currentPage.appendChild(clone)
                    self.toc.append({'h1':element.textContent, 'page':self.pageNumber})
                
                
                else:
                    if element.tagName.lower() == 'h1' :
                        self.headingsCount += 1
                        self.toc.append({'h1':element.textContent, 'page':self.pageNumber})
                    clone = element.cloneNode('true')
                    self.currentPage.appendChild(clone)
                    if self.currentPage.offsetHeight > self.targetHeigth:
                        self.currentPage.removeChild(clone)
                        self.createNewPage()
                        self.currentPage.appendChild(clone)
  
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
      print('parse_most_visible')
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
         print('READED')
         self.readed = True
      print(time() - self.open_time, self.min_time, self.mostVisible, self.pageNumber, self.readed_pages)

  #def scrollTo(self, **event):
  #      print('scroll_reader')
  #      element = document.getElementById(event['sender'].page)
  #      if element:
  #          element.scrollIntoView({'behavior': 'smooth', 'block': 'start'})
            
  def scroll_reader(self, page, *event):
        non_blocking.cancel(self.scroling_pages_info)
        self.scroling_pages_info = non_blocking.defer(self.parse_most_visible, 0.2)
        print('scroll_reader')


  def bookmark_click(self, sender, *event):
    print('bookmark_click')

  def toc_click(self, sender, *event):
    self.sidebar_social.hide()
    self.sidebar_toc.toggle()


  def social_click(self, sender, *event):
    self.sidebar_toc.hide()
    self.sidebar_social.toggle()



  def build_toc(self):
    
    
    for t in self.toc:
      link = Link(text=f"{t['h1']} стр.{t['page']}")

      heading = t['h1']
      if len(heading) > 17 : heading = heading[:17]
      pagen = str(t['page'])
      dots = '.' * (20 - len(heading) - len(pagen))
      link.text = '{}{}{}'.format(heading, dots, pagen)
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
    pass
    