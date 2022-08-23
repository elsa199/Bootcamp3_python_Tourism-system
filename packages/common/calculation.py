import math
from time import localtime, mktime


def calc_duration(start_date, end_date, st_count_clock: str, ed_count_clock: str):
    start_date_tuple = localtime(start_date)
    end_date_tuple = localtime(end_date)
    print(start_date_tuple)
    print(end_date_tuple)
    st_count_clock = [int(el) for el in st_count_clock.split(':')]
    ed_count_clock = [int(el) for el in ed_count_clock.split(':')]
    print(st_count_clock)
    print(ed_count_clock)
    if (start_date_tuple.tm_hour * 60 + start_date_tuple.tm_min) > (st_count_clock[0] * 60 + st_count_clock[1]): new_day = start_date_tuple.tm_mday + 1
    else: new_day = start_date_tuple.tm_mday
    new_start_date_tuple = tuple(
            [start_date_tuple.tm_year, start_date_tuple.tm_mon, new_day, st_count_clock[0], st_count_clock[1], 0, 0, 0, start_date_tuple.tm_isdst]
            )
    print(new_start_date_tuple)

    if (end_date_tuple.tm_hour * 60 + end_date_tuple.tm_min) > (ed_count_clock[0] * 60 + ed_count_clock[1]): new_day = end_date_tuple.tm_mday + 1
    else: new_day = end_date_tuple.tm_mday
    new_end_date_tuple = tuple(
            [end_date_tuple.tm_year, end_date_tuple.tm_mon, new_day, ed_count_clock[0], ed_count_clock[1], 0, 0, 0, end_date_tuple.tm_isdst]
            )
    print(new_end_date_tuple)

    start_date = mktime(new_start_date_tuple)
    end_date = mktime(new_end_date_tuple)

    duration = math.ceil((end_date - start_date)/86400)
    return [start_date, end_date, duration]