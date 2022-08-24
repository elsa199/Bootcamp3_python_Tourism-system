import random
import string

def id_generator(ids):
    while True:
        characters = string.ascii_letters + string.digits 
        id =  ''.join(random.choice(characters) for i in range(3))
        if id not in ids: return id