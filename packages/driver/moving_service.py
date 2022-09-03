import pandas as pd
from packages.utils.points import load_cities_data
from packages.common.generators import id_generator
from packages.common.input import inp
from packages.Bank.transaction import deposit
from packages.tourist.functions import gimmedates
from packages.common.clear import clear_console


class Intercity_services():
    """Intercity_services class is an user with Intercity services owner accessabilities.

    Intercity_services can 'register vehicle' to the database and then thier vehicle may be 'reserved' as a service to many tourists.
    """

    types = ['Bus', 'Train', 'Plane', 'Van','Car']
    def __init__(
        self, username: str, password: str, first_name: str, last_name: str,national_id: str, tel: str, **kwargs
    ) -> None: 
        self['username'] = username
        self['password'] = password
        self['first_name'] = first_name
        self['last_name'] = last_name
        self['national_id'] = national_id
        self['tel'] = tel
        return None

    def __setitem__(self,key,value):
        return setattr(self,key,value)
        
    def __getitem__(self,key):
        return getattr(self,key)

  

    def reservation(self, service_id: str, num: int) -> None:
        """reservation is a method of Intercity_services that can reserve a vehicle of targeted Intercity_services and deposit the price to his/her account.

        Args:
            service_id (str): id of specified service
            num (int): number of tourists to reserve
        """

        vehicles = pd.read_csv('./data/vehicles.csv', dtype=str)
        i = vehicles[vehicles.id == service_id].index 

        capacity = int(vehicles.iloc[i[0], vehicles.columns.get_loc('capacity')])
        vehicles.iloc[i[0], vehicles.columns.get_loc('capacity')] = capacity - num
        vehicles.to_csv('./data/vehicles.csv', index=False)

        rent = float(vehicles.iloc[i[0], vehicles.columns.get_loc('rent')])
        price = rent * num

        deposit(self['national_id'], price) 
        return
    
    def registeration(self) -> None:
        """registeration method of Intercity_services registers a new service for the called Intercity_services.

        """
        type = inp(
                f'{" - ".join(self["types"])}\nEnter your vehicle type between these items: ',
                "Please enter correctly: ",
                convert = lambda el: el.title(),
                key = lambda el: el in self['types']
            )
        capacity = inp("What is the capacity of your vehicle? ", "Please enter a number: ", key = lambda el: el.isnumeric())
        clear_console()
        addresses = load_cities_data(just='cities')
        print('\n !! Please pick your city only from this list of cities that we provide service in !!:')
        print(' - '.join(addresses))
        starting_city = inp("Where is the origin of your movement? ", "Please enter a city: ",convert = lambda el: el.title(), key = lambda el: el in addresses)
        destination_city = inp("Where is your destination? ", "Please enter a city: ", convert = lambda el: el.title(), key = lambda el: el in addresses)
        clear_console()

        start_datatime =  gimmedates(starting_city)


        rent = inp("How much it costs to rent your vehicle for one person: ", "Please enter a number: ", key = lambda el: el.isnumeric())
        avg_speed = inp("Please enter the average speed of your vehicle (in km/h)? ", "Please enter a number: ", key = lambda el: el.isnumeric())


        df = pd.read_csv('./data/vehicles.csv', dtype=str)
        id = id_generator(df.id.tolist())

        new_vehicle= pd.DataFrame(
            [[id, self['national_id'], type, capacity, starting_city, destination_city, start_datatime, rent, avg_speed, 'None', '0']],
            columns=[
                'id','moving_service_id','type','capacity','starting_city','destination_city','start_datatime','rent','avg_speed','score','num_score'
            ]
            )

        df = pd.concat([df, new_vehicle], axis=0, ignore_index=True)
        df.to_csv('./data/vehicles.csv', index=False) 
  


