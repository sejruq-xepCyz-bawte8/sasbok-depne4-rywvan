#Cheteme App
from .Browser import BrowserClass
from .Navigation import NavigationClass
from .Assets import AssetsClass
from .User import UserClass
from .Api import ApiClass
from .Settings import SettingsClass
from .Works import WorksClass
from .Awesome import AwesomeClass
from .Editor import EditorClass

print('ЧетеМе')

VERSION:int = 1

BROWSER:BrowserClass = None
ASSETS:AssetsClass = None
SETTINGS:SettingsClass = None
ORIGIN_API:str = None
ORIGIN_APP:str = None
NAVIGATION:NavigationClass = None
API:ApiClass = None
AW:AwesomeClass = None
WORKS:WorksClass = None
USER:UserClass = None
EDITOR:EditorClass = None

def init_app():
    global BROWSER
    global SETTINGS
    global ORIGIN_API
    global ORIGIN_APP
    global NAVIGATION
    global API
    global AW
    global WORKS
    global USER
    global EDITOR
    global ASSETS

    BROWSER = BrowserClass()
    SETTINGS = SettingsClass()

    ORIGIN_API = 'https://api.chete.me' if BROWSER.hostname == "chete.me" else 'http://192.168.0.101:8787'
    ORIGIN_APP = 'https://chete.me' if BROWSER.hostname == "chete.me" else 'http://192.168.0.101:3030'

    USER = UserClass()
    ASSETS = AssetsClass(origin=ORIGIN_APP)
    NAVIGATION = NavigationClass(fn_asset_get=ASSETS.get, is_author=USER.is_author)

    API = ApiClass(get_user=USER.get_user, origin=ORIGIN_API)

    AW = AwesomeClass(fn_asset_get=ASSETS.get)
    WORKS = WorksClass(fn_asset_get=ASSETS.get, fn_awesome_get=AW.get)

    if USER.is_author:
        EDITOR = EditorClass(fn_asset_get=ASSETS.get, author_id=USER.author_id)
    