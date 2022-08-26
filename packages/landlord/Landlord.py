import pandas as pd
from packages.common.generators import id_generator
from packages.common.input import inp
from packages.Bank.transaction import  deposit
from packages.utils.points import load_cities_data
from packages.common.clear import clear_console

class Landlord():
    types = ['Hotel', 'Apartment', 'Motel', 'Inn','Room', 'Villa']
    def __init__(self,username:str,password:str, first_name: str,last_name:str,national_id:str,tel: str,**kwargs) -> None:
        self['username']=username
        self['password']= password 
        self['first_name']= first_name
        self['last_name']=last_name
        self['national_id']=national_id
        self['tel']=tel
        return None
    def __setitem__(self,key,value):
        return setattr(self,key,value)
        
    def __getitem__(self,key):
        return getattr(self,key)
       
    def reservation(self, residence_id, duration):
        
        residences = pd.read_csv('./data/residences.csv', dtype=str)
        i = residences[residences.id == residence_id].index

        residences.iloc[i[0], residences.columns.get_loc('reserved')] = '1'
        residences.to_csv('./data/residences.csv', index=False)
        
        rent = float(residences.iloc[i[0], residences.columns.get_loc('rent')])
        price = rent * duration

        deposit(self['national_id'], price)
        return

    
    def registeration(self):
        type = inp(
            f'{" - ".join(self["types"])}\nEnter your residence type between these items: ',
            "Please enter correctly: ",
            convert = lambda el: el.title(),
            key = lambda el: el in self['types']
        )
        clear_console()
        addresses = load_cities_data(just='cities')
        print('\n !! Please pick your city only from this list of cities that we provide service in !!:')
        print(' - '.join(addresses))
        address = inp("Enter your residence city: ", "Don't leave it empty: ", convert = lambda el: el.title())
        clear_console()
        capacity = inp("How many people can stay in your residence: ", "Please enter a number: ", key = lambda el: el.isnumeric())
        rent = inp("How much it costs to rent your residence for one night: ", "Please enter a number: ", key = lambda el: el.isnumeric())
        df = pd.read_csv('./data/residences.csv', dtype=str)
        id = id_generator([el for el in df.id])
        new_residence = pd.DataFrame(
            [[id, self['national_id'], type, address, capacity, rent, '0', 'None', '0']],
            columns=['id','landlord_id','type','address','capacity','rent','reserved','score','no_scores']
        )
        df = pd.concat([df, new_residence], axis=0, ignore_index=True)
        df.to_csv('./data/residences.csv', index=False)





