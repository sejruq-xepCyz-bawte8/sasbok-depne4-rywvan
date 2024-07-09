from ._anvil_designer import Form_WelcomeTemplate
from anvil import *
import anvil.http
from anvil.js import window
from anvil_extras.storage import indexed_db
from anvil_extras import zod as z
import re
from ..App import init_app

schema_code = z.coerce.string().min(6).regex(re.compile(r"^[a-zA-Z\d\-_~@]+$"))

class Form_Welcome(Form_WelcomeTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    self.api = 'https://chete.me' if window.location.hostname == "chete.me" else 'http://192.168.0.101:8787'
  def form_show(self, **event):
    self.rich_welcome.content = WELCOME
    self.terms.content = TERMS
    
  def zod_code(self, sender, **event):
      sender.valid = schema_code.safe_parse(sender.text).success


  def input_change(self, **event):
    self.zod_code(self.tb_code)
    self.check_terms.foreground = '' if self.check_terms.checked else 'salmon'
    self.tb_code.border = '' if self.tb_code.valid else '1px solid LightSalmon'
    
    if self.check_terms.checked and self.tb_code.valid:
      self.button_enter.enabled = True
    else:
      self.button_enter.enabled = False

  def button_enter_click(self, **event):
 
    age = '1' if self.check_age.checked else '0'
    response = self.request_new_user(code=self.tb_code.text, age=age)
    
    if response:
      Notification("Успешен вход 🥳", style='success').show()

      store = indexed_db.create_store('cheteme-user')
      store['user'] = response
      init_app()
      open_form('Forms_Today.Today')

    else:
      Notification("Неуспешен вход 😭", style='danger').show()


  def request_new_user(self, code:str, age:str):
        headers:dict = {
        'Cheteme':'new_user',
        'Cheteme-User': 'new_user',
        'Cheteme-Code': code,
        'Cheteme-Age': age,
    }
      
        try:
            response = anvil.http.request(
                                    url=self.api,
                                    headers = headers,
                                    method='GET',
                                    json=True
                                    )
            
        except anvil.http.HttpError as e:
            response = None
            #status = e.status
        return response

  def b_terms_click(self, **event_args):
    self.rich_welcome.visible = not self.rich_welcome.visible
    self.terms.visible = not self.terms.visible
    
  

WELCOME = """
# ЧетеМе 1.0 бета
Онлайн читалище за творчеството на съвременни български писатели.

код за читатели *Chete@me*
"""

TERMS = """
## УСЛОВИЯ НА ПОЛЗВАНЕ:
##
## ЧетеМе (сайта)
- сайта не носи отговорност за публикуваните материали
- сайта не носи никаква отговорност за капацитета си
- при докладване на наручение, да проучи случая и да приеме адекватни мерки в приемлив период от време

## Авторите
- приемат да отразяват съдържанието дали е подходящо за непълнолетни
- да публикуват само и единствено лично творчество
- носят изцяло отговорност за публикуваните от тях творби
- съгласяват се да не публикуват не и/или противо законни текстове

## Права на текстовете/публикациите
- правата на публикациите са изцяло и единствено на съответния на творбата/публикацията автор
- читателите се съгласяват да не разпостраняват текстове и изображения от публикуваните произведения без съгласие на авторите
- читателите имат право да споделят линкове към произведенията предоставени от сайта без нужда от съгласие на авторите

## Технологични
- сайта използва "бисквитки/cookies"
- не е позволено ползване на информация от сайта по друг начин освен чрез интерфейса
- не е позволено ползването на програмни инструменти за извличане и/или управление на сайта

"""