import pandas as pd
from packages.common.generators import id_generator
from packages.common.input import inp
from packages.Bank.transaction import deposit
from packages.tourist.functions import gimmedates

class Intercity_services():

    types = ['Bus', 'Train', 'Plane', 'Won','Car']
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

  

    def reservation(self, service_id, num):

        vehicles = pd.read_csv('data/vehicles.csv', dtype=str)
        print(vehicles)
        i = vehicles[vehicles.id == service_id].index 
        print(i)

        capacity = int(vehicles.iloc[i[0], vehicles.columns.get_loc('capacity')])
        print(capacity)
        vehicles.iloc[i[0], vehicles.columns.get_loc('capacity')] = capacity - num
        print(vehicles)
        vehicles.to_csv('data/vehicles.csv', index=False)

        rent = float(vehicles.iloc[i[0], vehicles.columns.get_loc('rent')])
        price = rent * num

        deposit(self.national_id, price) 
        print(123123)
        return
    
    def registeration(self): 
        type = inp(
                f'{" - ".join(self["types"])}\nEnter your vehicle type between these items: ',
                "Please enter correctly: ",
                convert = lambda el: el.title(),
                key = lambda el: el in self['types']
            )
        capacity = inp("What is the capacity of your vehicle? ", "Please enter a number: ", key = lambda el: el.isnumeric())
        starting_city = inp("Where is the origin of your movement? ", "Please enter a city: ",convert = lambda el: el.title())
        destination_city = inp("Where is your destination? ", "Please enter a city: ", convert = lambda el: el.title())

        start_datatime =  gimmedates(starting_city)


        rent = inp("How much it costs to rent your vehicle for one person: ", "Please enter a number: ", key = lambda el: el.isnumeric())
        avg_speed = inp("Please enter the average speed of your vehicle (in km/h)? ", "Please enter a number: ", key = lambda el: el.isnumeric())


        df = pd.read_csv('data/vehicles.csv', dtype=str)
        id = id_generator(df.id.tolist())

        new_vehicle= pd.DataFrame(
            [[id, self['national_id'], type, capacity, starting_city, destination_city, start_datatime, rent, avg_speed, 'None', '0']],
            columns=[
                'id','moving_service_id','type','capacity','starting_city','destination_city','start_datatime','rent','avg_speed','score','num_score'
            ]
            )

        df = pd.concat([df, new_vehicle], axis=0, ignore_index=True)
        df.to_csv('data/vehicles.csv', index=False) 
  


