import binascii
import hashlib
import os
from scripts.db_link import *
from scripts.sci_discover import *


def get_bearer_code():
    return get_discover_bearer_code()


def login(email, password):
    if authenticate(email, password):
        return True
    else:
        return False
