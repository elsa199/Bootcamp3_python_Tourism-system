import json
import pandas as pd
from packages.utils.env import main as initialize

def login(inputs):
    path = f'./data/{inputs["type"]}s.json'
    fObj = open(path)
    jdict = json.load(fObj)
    users = pd.json_normalize(jdict)
    while True:
        # Check username and password initialize(True)
        try:
            i = users.username.tolist().index(inputs['username'])
            if users.password.tolist()[i] == inputs['password']:
                print("Wellcome... What's your command? :)")
                user = users.iloc[i].to_dict()
                break
            else: raise Exception('I')
        except Exception as e:
            print("***************\nWrong username and password. Please try again.\n***************\n")
            return False
    if inputs['type'] == 'tourist':
        from packages.tourist.Class import Tourist
        return Tourist(**user)
    if inputs['type'] == 'admin':
        from packages.admin.Class import Admin
        return Admin(**user)
