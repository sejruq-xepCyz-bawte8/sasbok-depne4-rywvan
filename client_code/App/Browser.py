import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from anvil.js import window

#"loadingSpinner"
delete = ["anvil-header", "anvil-badge", "error-indicator"]

class BrowserClass:
    def __init__(self):
        self.origin = window.location.origin
        self.protocol = window.location.protocol
        self.host = window.location.host
        self.hostname = window.location.hostname

  