import pandas as pd


def withdraw(id: str, price: float) -> None:
    """withdraw function is used to withdraw money from specified account.

    Args:
        id (str): Target account id.
        price (float | int): The ammount of withdrawal.

    Raises:
        Exception: If the specified account has not enough money, the function raises a Exception.
    """
    accounts = pd.read_csv('./data/accounts.csv', dtype=str)
    balance = float(
        accounts.loc[accounts[accounts['owner_id'] == id].index[0], 'deposit'])
    if balance >= price:
        balance -= price
        accounts.loc[(accounts['owner_id'] == id).index[0], 'deposit'] = balance
        accounts.to_csv('./data/accounts.csv', index=False)
    else:
        raise Exception('Not enough balance.')


def deposit(id: str, price:float)->None:
    """deposit function is used to deposit money to specified account.

    Args:
        id (str): Target account id.
        price (float | int): The ammount of deposition.

    Raises:
        Exception: If the amount is more than one million, the function raises a Exception.
    """
    accounts = pd.read_csv('./data/accounts.csv', dtype=str)
    balance = float(
        accounts.loc[accounts[accounts['owner_id'] == id].index[0], 'deposit'])
    if price <= 10000000.0:
        balance += price
        accounts.loc[(accounts['owner_id'] == id), 'deposit'] = balance
        accounts.to_csv('./data/accounts.csv', index=False)
    else:
        raise Exception('Limit reached.')
