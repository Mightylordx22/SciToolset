from scripts.admin_tools import get_codes, gen_unique_code
from scripts.db_link import authenticate, get_user_data, get_user_id
from scripts.login import get_auth_data, get_auth_token
from scripts.register import register_user
from scripts.sci_discover import auth_discover_bearer_token


def register(email, password, unique_code, f_name, l_name):
    return register_user(email, password, unique_code, f_name, l_name)


def login(email, password):
    return authenticate(email, password)


def get_authenticate_data(token):
    return get_auth_data(token)


def get_authenticate_token(secret, u_id):
    return get_auth_token(secret, u_id)


def authenticate_discover_bearer_token():
    auth_discover_bearer_token()

def genarate_unique_code(is_admin):
    gen_unique_code(is_admin)


def get_unique_codes():
    return get_codes()


def get_user(u_id):
    return get_user_data(u_id)


def get_user_id_from_token(token):
    return get_user_id(token)
