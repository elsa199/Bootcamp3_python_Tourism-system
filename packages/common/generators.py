import random
import string

def id_generator():
    characters = string.ascii_letters + string.digits 
    return ''.join(random.choice(characters) for i in range(10))