import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from anvil_extras import zod as z
import re
from anvil_extras.hashlib import sha256

schema_url = z.coerce.string().min(3).regex(re.compile(r"^[a-zA-Z\d\-_~]+$")) #@$!%*?&#
schema_title = z.coerce.string().min(3)
schema_code = z.coerce.string().min(6).regex(re.compile(r"^[a-zA-Z\d\-_~@]+$"))
schema_device_code = z.coerce.string().len(8).regex(re.compile(r"^[a-zA-Z\d\-_~@]+$"))

def zod_uri(sender):
    sender.valid = schema_url.safe_parse(sender.text).success
    sender.border = "1px solid LightGreen" if sender.valid else "1px solid LightSalmon"

def title_zod(sender):

    sender.valid = schema_title.safe_parse(sender.text).success
    sender.border = "1px solid LightGreen" if sender.valid else "1px solid LightSalmon"

def zod_code(sender):
    sender.valid = schema_code.safe_parse(sender.text).success
    

def zod_device_code(sender):
    sender.valid = schema_device_code.safe_parse(sender.text).success





def hash_args(*args)->str:
    string = ''
    for arg in args:
        string += str(arg)
    hash_hex = sha256(string)

    return hash_hex