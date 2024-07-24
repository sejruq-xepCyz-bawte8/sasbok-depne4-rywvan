#Cheteme Index Module
from anvil import *
from anvil_extras.storage import indexed_db
from . import init_app
from anvil_extras import non_blocking
import anvil.http

def has_user():
    store = indexed_db.create_store('cheteme-user')
    return bool(store.get('user'))

def main():
    init_app()
    open_form('Forms_Today.Today')

def no_user():
    open_form('Form_Welcome')




if __name__ == '__main__':
    if has_user():
        main()
    else:
        no_user()