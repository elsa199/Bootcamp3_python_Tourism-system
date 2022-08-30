import math
from time import localtime, mktime
import pandas as pd

def calc_duration(start_date: float, end_date: float, st_count_clock: str, ed_count_clock: str) -> list:
        """calc_duration calcuates stayed in hotel days.

        This function takes an arriving and leaving time in seconds format and also takes the entry and exit clock of hotel rooms, then calculates the days in which the passengers are counted to be stayed in the hotel room

        Args:
            start_date (float | int): Arriving time in seconds.
            end_date (float | int): Leaving time in seconds.
            st_count_clock (str): Room entry in format of 'hh:mm'.
            ed_count_clock (str): Room exit in format of 'hh:mm'.

        Returns:
            list: new start date in seconds format, new end date in seconds format and days between them in int format.
        """
        start_date_tuple = localtime(start_date)
        end_date_tuple = localtime(end_date)
        st_count_clock = [int(el) for el in st_count_clock.split(':')]
        ed_count_clock = [int(el) for el in ed_count_clock.split(':')]
        if (start_date_tuple.tm_hour * 60 + start_date_tuple.tm_min) > (st_count_clock[0] * 60 + st_count_clock[1]): new_day = start_date_tuple.tm_mday + 1
        else: new_day = start_date_tuple.tm_mday
        new_start_date_tuple = tuple(
                [start_date_tuple.tm_year, start_date_tuple.tm_mon, new_day, st_count_clock[0], st_count_clock[1], 0, 0, 0, start_date_tuple.tm_isdst]
                )

        if (end_date_tuple.tm_hour * 60 + end_date_tuple.tm_min) > (ed_count_clock[0] * 60 + ed_count_clock[1]): new_day = end_date_tuple.tm_mday + 1
        else: new_day = end_date_tuple.tm_mday
        new_end_date_tuple = tuple(
                [end_date_tuple.tm_year, end_date_tuple.tm_mon, new_day, ed_count_clock[0], ed_count_clock[1], 0, 0, 0, end_date_tuple.tm_isdst]
                )

        start_date = mktime(new_start_date_tuple)
        end_date = mktime(new_end_date_tuple)

        duration = math.ceil((end_date - start_date)/86400)
        return [start_date, end_date, duration]


def calc_arrive_date(starting_city,destination_city,start_datatime,avg_speed):
        cities = pd.read_csv('./data/cities.csv', header=None)
        distances = pd.read_csv('./data/distances.csv', header=None)
        start_index = cities[cities[0] == starting_city].index[0]
        destination_index = cities[cities[0] == destination_city].index[0]
        distance = distances[start_index][destination_index]
        duration = distance * avg_speed
        destination_date = start_datatime + duration * 60 * 60
        return destination_date