from os import times
from os import uname 
from dataclasses import dataclass
from email.generator import DecodedGenerator
from datetime import timedelta, time, date
import datetime as dt
from tabnanny import check
from time import strftime
import os
import _strptime
import pandas as pd
from packages.common.generators import id_generator
from packages.common.input import inp
from packages.Bank.transaction import deposit


class Intercity_services():

  types = ['Bus', 'Train', 'Plane', 'Won','Car']
         #service_id, end_date, price, staus                    
  def __init__(
      self, username: str, password: str, first_name: str, last_name: str,
      national_id: str, tel: str, **kwargs) -> None: 

      self.username = username
      self.password = password
      self.first_name = first_name
      self.last_name = last_name
      self.national_id = national_id
      self.tel = tel


  def __setitem__(self,key,value):
      return setattr(self,key,value)
        
  def __getitem__(self,key):
      return getattr(self,key)

  

  def reservation(self, service_id, num):

    vehicle = pd.read_csv('./data/vehicle.csv', dtype=str)
    i = vehicle[vehicle.Id == service_id].index 
    capacity = int(vehicle.iloc[i[0], vehicle.columns.get_loc('capacity')])
    vehicle.iloc[i[0], vehicle.columns.get_loc('capacity')] = capacity - num
    vehicle.to_csv('./data/vehicle.csv', index=False)

    rent = int(vehicle.iloc[i[0], vehicle.columns.get_loc('rent')])
    price = rent * num
    deposit(self.national_id, price) 

    
  def registeration(self): 
    type = inp(
            f'{" - ".join(self["types"])}\nEnter your vehicle type between these items: ',
            "Please enter correctly: ",
            convert = lambda el: el.title(),
            key = lambda el: el in self['types']
        )
    capacity = inp("What is the capacity of your vehicle? ", "Please enter a number: ", key = lambda el: el.isnumeric())
    starting_city = inp("Where is the origin of your movement?? ", "Please enter a city: ")
    destination_city = inp("Where is your destination? ", "Please enter a city: ")
    Start_datatime =  inp("Please enter the start time of your trip ", "Please enter a date and time: ")
    end_datetime = inp("Please enter the end time of your trip ", "Please enter a date and time: ")
    rent = inp("How much it costs to rent your vehicle for one person: ", "Please enter a number: ", key = lambda el: el.isnumeric())
    avg_speed = inp("Please enter the average speed of your vehicle ", "Please enter a number: ", key = lambda el: el.isnumeric())
    id = id_generator()
    new_vehicle= pd.DataFrame(
        [[id, self.national_id, type, capacity, starting_city, destination_city, Start_datatime, end_datetime, rent, 0, None, 0]],
        columns=['id','national_id','type_vehivle','capacity','starting_city','destination_city','Start_datatime','end_datetime','rent'
        ,'avg_speed','avg_ Score','num_score']
        )

    df = pd.read_csv('./data/vehicle.csv', dtype=str)
    df = pd.concat([df, new_vehicle], axis=0, ignore_index=True)
    df.to_csv('./data/vehicle.csv', index=False) 
  


