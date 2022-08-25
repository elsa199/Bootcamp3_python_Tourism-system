import random
import string
import numpy as np

def id_generator(ids: np.ndarray):
    """_summary_

    Args:
        ids (np.ndarray): _description_

    Returns:
        _type_: _description_
    """

    while True:
        characters = string.ascii_letters + string.digits 
        id =  ''.join(random.choice(characters) for i in range(3))
        if id not in ids: return id