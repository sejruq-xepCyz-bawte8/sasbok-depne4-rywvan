from anvil import *
from anvil.js.window import jQuery as jQ


class NavigationClass:
    def __init__(self, fn_asset_get, fn_is_author):
        self.element = jQ('#navigation')
        self.asset = fn_asset_get
        self.forms:dict = self.asset(file_path='navigation/nav_forms.json')
        self.navbars = self.asset(file_path='navigation/nav_bars.json')
        self.is_author = fn_is_author
       

    def set(self, nav_bar:str):
        if self.is_author and self.navbars.get(f'{nav_bar}_author'):
            file_path = self.navbars.get(f'{nav_bar}_author')
        else:
            file_path = self.navbars.get(nav_bar)
        html:str = self.asset(file_path)
        self.element.html(html)


    def open_form(self, sender, **event):
        self.element.children().removeClass('active')
        sender_id:str = sender.attr('id')
        form_name:str = self.forms[sender_id]
        if sender_id in self.navbars:
            #need to set navbar
            self.set(nav_bar=sender_id)
            open_form(form_name)
        else:
            #just open form
            sender.addClass('active')
            open_form(form_name)
        



    def delete(self):
        self.element.html('')