import pandas as pd

def withdraw(id, price):
    accounts= pd.read_csv('data/accounts.csv', dtype=str)
    balance= float(accounts.loc[accounts[accounts['owner_id'] == id].index[0], 'deposit'])
    if balance >= price:
        balance -= price
        accounts.loc[(accounts['owner_id']== id), 'deposit']= balance
        accounts.to_csv('data/accounts.csv', index=False)
    else:
        raise Exception('Not enough balance.')

def deposit(id,price):
    accounts = pd.read_csv('data/accounts.csv', dtype=str)
    balance = float(accounts.loc[accounts[accounts['owner_id'] == id].index[0], 'deposit'])
    if price <= 10000000.0:
        balance += price
        accounts.loc[(accounts['owner_id']== id), 'deposit'] = balance
        accounts.to_csv('data/accounts.csv', index=False)
    else:
        raise Exception('Limit reached.')
