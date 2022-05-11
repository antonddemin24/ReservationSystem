from datetime import datetime, date
from datetime import timedelta


def check(row, new_date_in, new_date_out):
    lst = row[2].split(',')
    date1 = date(int(lst[0]), int(lst[1]), int(lst[2]))
    lst = row[3].split(',')
    date2 = date(int(lst[0]), int(lst[1]), int(lst[2]))
    lst = new_date_in.split(',')
    date3 = date(int(lst[0]), int(lst[1]), int(lst[2]))
    lst = new_date_out.split(',')
    date4 = date(int(lst[0]), int(lst[1]), int(lst[2]))
    while date1 != date2:
        if date3 == date1 or date4 == date1:
            return False
        date1 = date1 + timedelta(days=1)
    return True
