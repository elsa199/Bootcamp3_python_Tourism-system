from time import mktime, localtime
import pandas as pd

def update_travels():
    active_travels = pd.read_csv('./data/active_travels.csv', dtype=str)
    done_travels = pd.read_csv('./data/travels.csv', dtype=str)
    done_travels = pd.concat([done_travels, active_travels[[int(el) < mktime(localtime()) for el in active_travels.end]]], axis = 0, ignore_index=True)    
    done_travels.to_csv('./data/travels.csv', index= False)
    print(done_travels)
    active_travels = active_travels.drop(active_travels[[int(el) < mktime(localtime()) for el in active_travels.end]].index)
    active_travels.to_csv('./data/active_travels.csv', index= False)
