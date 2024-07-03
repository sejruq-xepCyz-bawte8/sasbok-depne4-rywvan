#Cheteme Index Module
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from anvil_extras.storage import indexed_db
from . import init_app

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