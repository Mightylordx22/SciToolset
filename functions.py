import hashlib
import binascii


def is_logged_in(debug):
    if debug == 1:
        return True
    else:
        return False


def check_password(user_password, stored_password):
    """
    A function that checks to see if the user's password is correct or not
    :param user_password: The password the user enters
    :param stored_password: The password that userPassword is being checked against
    :return: True or False
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pass_hash = hashlib.pbkdf2_hmac('sha512', user_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pass_hash = binascii.hexlify(pass_hash).decode('ascii')
    return pass_hash == stored_password


def hash_password(password):
    """
    A function that hashes a password the user enters
    :param password: The password the user enters
    :return: Hashed version of the password
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pass_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pass_hash = binascii.hexlify(pass_hash)
    return (salt + pass_hash).decode('ascii')
