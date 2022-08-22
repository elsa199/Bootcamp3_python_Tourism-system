from os import times
from email.generator import DecodedGenerator
from datetime import timedelta, time, date
import datetime as dt
from time import strftime
import os
import _strptime
import pandas as pd


def search(number, beginning, destination, date ):
  
  output_file= pd.DataFrame()
  index_list=[]
  ifile2= ifile.drop('national_number',axis=1)

    for x in range(len(beginning)):
        for i in ifile[ifile['starting_city']== beginning[x]].index.values:
            for j in ifile[ifile['destination_city']== destination[x]].index.values:
                for k in ifile[ifile['start_date&time']== date[x]].index.values:
                    for m in ifile[ifile['capacity']>= number].index.values:
                        if i==j==k==m:
                            index_list.append(i)
                        
    print(index_list)
    for i in index_list:
        output_file= output_file.append(ifile2.loc[i])
    print(output_file)
    request= int(input('Please enter the desired service number: '))
    return 


from os import uname 
 #init function must => create a driver - reads services.csv and filter the services which driver is responsible for.
class Intercity_services():                             # Must have init function to make a driver by making an instance
                                   # Imports out of class
 from dataclasses import dataclass
 from email.generator import DecodedGenerator
 from datetime import timedelta
 from datetime  import  date
 from os import times
 import datetime as dt
 from time import strftime
 import _strptime
 from datetime import time

 Final_output={                                       # Must be 2 csv files => Ms. Kazemi will give the columns
     "Users":{},
     "Services":{},
     "Scores":{}
               }
 Vehicle_information={                                # Must be above the init function
     "bus":{"capacity":40,"speed":60},
     "van":{"capacity":7,"speed":70},
     "car":{"capacity":4,"speed":80},
     "minibus":{"capacity":15,"speed":65}
     }
                              # Register user should be an independent function and writes to a file (drivers.csv file)
 def Register_user(self,Firts_name,Last_name,National_code,Phone_number):
#check duplicate national code
  if National_code in self.Final_output["Users"]:
    print("You have already registered")
    return False
  else:
   #save user information
   self.Final_output["Users"][National_code]={
       "Firts_name":Firts_name,
       "Last_name":Last_name,
       "Phone_number":Phone_number,
       }
   return True


 def Register_service(self,National_code,Vehicle_type,Origin,Destination,Departure_date,Departure_time,Return_date,Return_time,Price_per_person,Number_of_passengers):  
   #requirements 1 
   #create service id
   Service_id=len( self.Final_output["Services"])+1 # Create a random id with a specific length
   #save service information
   self.Final_output["Services"][Service_id]={      # Good but *also* save it into a file (services.csv)
           "User_national_code":National_code,
           "Vehicle_type":Vehicle_type,
           "Origin":Origin,
           "Destination":Destination,
           "Departure_date":Departure_date,
           "Departure_time":Departure_time,
           "Return_date":Return_date,
           "Return_time":Return_time,
           "Price_per_person":Price_per_person,
           "Number_of_passengers":Number_of_passengers
       }
   return Service_id
  

 def Reservation(self,Service_id):
# requirements 6
   Service=self.Final_output["Services"][Service_id]
   Total_price=Service["Number_of_passengers"]*Service["Price_per_person"]
   Confirm=input(f"The cost of service is {Total_price}. Do you confirm? (y/n)")
   if Confirm=='y':
    self.Final_output["Services"][Service_id]["Total_price"]=Total_price

# requirements 3,4
   S=self.Vehicle_information[Service["Vehicle_type"]]["capacity"]
   while True:
    if  S==0:
      print('reservation are not posible due to full capecity')
      break
    elif int(Service["Number_of_passengers"])>int(S):
     return f"sorry the vehicle has only",int(S),"spaces"           # Return more casual
    else:
     S=S-Service["Number_of_passengers"]
     return f"The vehicle has enough capacity"                      # Return more casual
      
  #requirements 2
    from datetime import datetime,timedelta,time
    DD1=self.dt.datetime.strptime(Service["Departure_date"],"%d.%m.%Y")
    DR1=self.dt.datetime.strptime(Service["Return_date"],"%d.%m.%Y")
    TR1=self.datetime.strptime(Service["Return_time"],"%H.%M.%S")
    TD1=self.datetime.strptime(Service["Departure_time"],"%H.%M.%S")

    if self.Vehicle_information[Service["Vehicle_type"]]=='bus':
         if Service["Distance"]<=60:
          day=DD1.date()+timedelta(days=1)
          timee=TD1+timedelta(hours=6)
          #print(day,timee)
          self.Final_output["Services"][Service_id]["arrival date"]=day
          self.Final_output["Services"][Service_id]["arriving time"]=timee

         else:
          day=DD1.date()+timedelta(days=1)
          timee=TD1+timedelta(hours=3)
          #print(day,timee)
          self.Final_output["Services"][Service_id]["arrival date"]=day
          self.Final_output["Services"][Service_id]["arriving time"]=timee

    if self.Vehicle_information[Service["Vehicle_type"]]=='car' :
         if Service["Distance"]<=80:
          day=DD1.date()+timedelta(days=0)
          timee=TD1+timedelta(hours=4)
          #print(day,timee)
          self.Final_output["Services"][Service_id]["arrival date"]=day
          self.Final_output["Services"][Service_id]["arriving time"]=timee

         else:
          day=DD1.date()+timedelta(days=0)
          timee=TD1+timedelta(hours=10)
          #print(day,timee)
          self.Final_output["Services"][Service_id]["arrival date"]=day
          self.Final_output["Services"][Service_id]["arriving time"]=timee

    if self.Vehicle_information[Service["Vehicle_type"]]=='van' :
        if Service["Distance"]<=70:
         day=DD1.date()+timedelta(days=0)
         timee=TD1+timedelta(hours=8)
         #print(day,timee)
         self.Final_output["Services"][Service_id]["arrival date"]=day
         self.Final_output["Services"][Service_id]["arriving time"]=timee

        else:
         day=DD1.date()+timedelta(days=1)
         timee=TD1+timedelta(hours=6)
         #print(day,timee)
         self.Final_output["Services"][Service_id]["arrival date"]=day
         self.Final_output["Services"][Service_id]["arriving time"]=timee

    if self.Vehicle_information[Service["Vehicle_type"]]=='minibus' :
        if Service["Distance"]<=65:
         day=DD1.date()+timedelta(days=0)
         timee=TD1+timedelta(hours=12)
         #print(day,timee)
         self.Final_output["Services"][Service_id]["arrival date"]=day
         self.Final_output["Services"][Service_id]["arriving time"]=timee
        else:
         day=DD1.date()+timedelta(days=1)
         timee=TD1+timedelta(hours=9)
        # print(day,timee)
         self.Final_output["Services"][Service_id]["arrival date"]=day 
         self.Final_output["Services"][Service_id]["arriving time"]=timee 

 # requirements 5
    y1 = str(DR1.year)
    m1 = str(DR1.month)
    d1 = str(DR1.day)
    y2 = str(day.year)
    m2 = str(day.month)
    d2 = str(day.day)
    h1=str(TR1.hour)
    m1=str(TR1.minute)
    s1=str(TR1.second)
    h2=str(timee.hour)
    m2=str(timee.minute)
    s2=str(timee.second)

    if y1<y2:
     print('sorry date of return is not logical.')
    elif y1==y2 & m1<m2:
     print('sorry date of return is not logical.') 
    elif y1==y2 & m1==m2 & d1<d2:
     print('sorry date of return is not logical.')
    else:
      if h1>=h2 & m1>=m2 & s1>=s2:
         print('time & date of return are true.')
      else:
        print('time of return is not true.')    
  
  #return True
#   else:
   # return False
  

 def Register_comment(self,Service_id):                   # Given inputs -> an integer between 1 and 5
    # requirements 7                                      # Store it as a property of service into the services.csv file
    Service=self.Final_output["Services"][Service_id]
    Current_rate=int(input('please rate this service form 1 to 5:'))
    if Service_id not in self.Final_output["Scores"]:
     self.Final_output["Scores"][Service_id]={"Rate_count":1,"rate":Current_rate}
    else:
     Rate_count=self.Final_output["Scores"][Service_id]["Rate_count"]
     Old_rate=self.Final_output["Scores"][Service_id]["rate"]
     New_rate=(Old_rate*Rate_count+Current_rate)/(Rate_count+1)
     Rate_count=Rate_count+1
     self.Final_output["Scores"][Service_id]={"Rate_count":Rate_count,"rate":New_rate}
    return True
   
