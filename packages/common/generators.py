import random
import string

def id_generator(ids: list)-> str:
    """id_generator returns a random string of 'ascii letters' with length of 3.

    Args:
        ids (list): A list to check uniqueness of created id in among them.

    Returns:
        str: Three character lengthed string.
    """
    while True:
        characters = string.ascii_letters + string.digits 
        id =  ''.join(random.choice(characters) for i in range(3))
        if id not in ids: return id