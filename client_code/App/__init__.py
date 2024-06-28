#Cheteme App
from .Browser import BrowserClass
from .Navigation import NavigationClass
from .Assets import AssetsClass
from .User import UserClass
from .Api import ChetemeApi
print('init app')

PRODUCTION = False
VERSION = 1
BROWSER = BrowserClass()
ORIGIN_API = 'https://chete.me' if PRODUCTION else 'http://192.168.0.101:8780'
ORIGIN_APP = 'https://chete.me' if PRODUCTION else 'http://192.168.0.101:3030'
USER = UserClass()
ASSETS = AssetsClass(origin=ORIGIN_APP)
NAVIGATION = NavigationClass(fn_asset_get=ASSETS.get)

API = ChetemeApi(get_user=USER.get_user, origin=ORIGIN_API)


    