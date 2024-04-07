from dataclasses import dataclass


@dataclass
class Message:
    """
    dataclass for Message
    """
    string: str
    k: int
    delimiter: str = ' '