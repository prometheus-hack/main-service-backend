class BaseCryptoMSDU:
    """
    class that describes any CryptoSystem
    encrypt_function is partial solution of MSDU using as encode function
    private_key is secret key for encode and decode
    decrypt_function is function to decrypt message
    for async systems
    U is module
    w is open key
    v is another private key
    """

    encrypt_function = None
    secret_key = None
    decrypt_function = None

    @classmethod
    def encrypt(cls, msg: int) -> int:
        return cls.encrypt_function(msg, cls.secret_key)

    @classmethod
    def decrypt(cls, msg: int) -> int:
        return cls.decrypt_function(msg, cls.secret_key)