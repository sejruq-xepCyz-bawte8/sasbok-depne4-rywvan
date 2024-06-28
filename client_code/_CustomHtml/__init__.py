from ._anvil_designer import _CustomHtmlTemplate
from anvil import *


class _CustomHtml(_CustomHtmlTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
