#Cheteme App
from .Browser import BrowserClass
from .Navigation import NavigationClass
from .Assets import AssetsClass
from .User import UserClass
from .Api import ChetemeApi
from .Settings import SettingsClass
from .Works import WorksClass
from .Awesome import AwesomeClass
from Editor import EditorClass
print('ЧетеМе')


VERSION = 1
BROWSER = BrowserClass()
SETTINGS = SettingsClass()

ORIGIN_API = 'https://api.chete.me' if BROWSER.hostname == "chete.me" else 'http://192.168.0.101:8787'
ORIGIN_APP = 'https://chete.me' if BROWSER.hostname == "chete.me" else 'http://192.168.0.101:3030'

USER = UserClass()
ASSETS = AssetsClass(origin=ORIGIN_APP)
NAVIGATION = NavigationClass(fn_asset_get=ASSETS.get, fn_is_author=USER.check_is_author)


API = ChetemeApi(get_user=USER.get_user, origin=ORIGIN_API)

AW = AwesomeClass(fn_asset_get=ASSETS.get)
WORKS = WorksClass(fn_asset_get=ASSETS.get, fn_awesome_get=AW.get)
EDITOR = EditorClass(fn_asset_get=ASSETS.get, fn_user_get=USER.get_user)
    