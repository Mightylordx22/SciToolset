from scripts.db_link import *
from scripts.sci_discover import *


def get_bearer_code():
    authenticate("a", "a")
    return get_discover_bearer_code()
