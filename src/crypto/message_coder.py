from typing import Type

from .crypto_system import BaseCryptoMSDU
from .k_gram_coder import KGramCoder
from .message import Message


class MessageCoder:
    """
    class for code or decode Message
    """

    @staticmethod
    def encode(msg: Message, encrypter_class: Type[BaseCryptoMSDU], k_gram_coder: Type[KGramCoder]):
        k_gram_list = [msg.string[i:i+2] for i in range(0, len(msg.string), msg.k)]
        return msg.delimiter.join(map(lambda x: str(encrypter_class.encrypt(x)),
                                      [k_gram_coder.encode(k_gram) for k_gram in k_gram_list]))

    @staticmethod
    def decode(msg: Message, decrypter_class: Type[BaseCryptoMSDU], k_gram_coder: Type[KGramCoder]):
        encrypted_k_gram_list = list(map(int, msg.string.split(msg.delimiter)))
        return ''.join([k_gram_coder.decode(decrypter_class.decrypt(int(encrypted_k_gram)))
                        for encrypted_k_gram in encrypted_k_gram_list])