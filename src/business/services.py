from crypto.services import decrypt
from jwtauth.repositories import UserRepository, ObjectDoesNotExist


def qr_prove(cryptred_str):
    try:
        data = decrypt(cryptred_str)
    except Exception:
        return None
    try:
        email = data
        return UserRepository.get(email)
    except (KeyError, ObjectDoesNotExist):
        return None
