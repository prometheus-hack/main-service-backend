from ast import literal_eval

from crypto.crypto_system import BaseCryptoMSDU
from crypto.k_gram_coder import KGramCoder
from crypto.message import Message
from crypto.message_coder import MessageCoder


def encrypt_function(msg: int, key: int) -> int:
    power = 5
    return (msg + 3 * key) ** power + (9 * msg + 4 * key) ** power + (12 * msg + 19 * key) ** power + (
            28 * msg + 21 * key) ** power + (31 * msg + 36 * key) ** power + (39 * msg + 37 * key) ** power - (
            4 * msg + 9 * key) ** power - (19 * msg + 12 * key) ** power - (21 * msg + 28 * key) ** power - (
            36 * msg + 31 * key) ** power - (37 * msg + 39 * key) ** power


def decrypt_function(coded_msg: int, key: int) -> int:
    return int(coded_msg ** (1 / 5) - key) // 3


class SymmMSDUPowerFive(BaseCryptoMSDU):
    encrypt_function = encrypt_function
    secret_key = 9
    decrypt_function = decrypt_function


class BiGramCoder(KGramCoder):
    k = 2
    alphabet_power = 128


def encrypt(data):
    str_data = str(data)
    if len(str_data) % 2:
        str_data += ' '
    base_msg = Message(str_data, 2)
    return MessageCoder.encode(base_msg, SymmMSDUPowerFive, BiGramCoder)


def decrypt(st):
    return literal_eval(MessageCoder.decode(Message(st, 2), SymmMSDUPowerFive, BiGramCoder))
