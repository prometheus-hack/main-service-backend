class KGramCoder:
    """
    class to describe any k-grams coding,
    step is ascii letter that start in ur alphabet(better user ord(letter)),
    alphabet power is length of your alphabet,
    alphabet - just for add or override codes,
    use_default_alphabet - if True using ansi coding(and adding your alphabet), else you need to describe your alphabet
    """
    k: int = None
    start_symbol: int = 1
    alphabet_power: int = None
    alphabet: dict = {}
    use_default_alphabet: bool = True

    @classmethod
    def encode(cls, k_gram: str) -> int:
        if cls.use_default_alphabet:
            return sum([cls.alphabet_power ** i * (ord(char) - cls.start_symbol) if char not in
                                                                                    cls.alphabet else
                        cls.alphabet_power ** i * cls.alphabet[char] for i, char in enumerate(list(k_gram[::-1]))])
        else:
            return sum([cls.alphabet_power ** i * cls.alphabet[char] for i, char in enumerate(list(k_gram[::-1]))])

    @classmethod
    def decode(cls, encrypted_k_gram: int) -> str:
        alphabet_codes = dict((v, k) for k, v in cls.alphabet.items())
        k_gram_list = []
        for i in range(cls.k):
            if cls.use_default_alphabet:
                res = encrypted_k_gram % cls.alphabet_power
                if res in alphabet_codes.keys():
                    k_gram_list.append(alphabet_codes[res])
                else:
                    k_gram_list.append(str(chr(res + cls.start_symbol)))
            else:
                k_gram_list.append(str(alphabet_codes[encrypted_k_gram % cls.alphabet_power]))
            encrypted_k_gram //= cls.alphabet_power

        return ''.join(k_gram_list)[::-1]