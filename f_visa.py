import re
import pandas as pd
from datetime import time, datetime as dt
from calendar import monthrange
from fiscalyear import FiscalDate, FiscalDateTime

PATH = "Z:/Internal/clearing/Visa/"

quarter_months = [
    ['01', '02', '03'],
    ['04', '05', '06'],
    ['07', '08', '09'],
    ['10', '11', '12']
]

months = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12]
]


def check_quarter():
    a = FiscalDate.today()
    # a = FiscalDateTime(2023, 1, 1, 0, 0) # check what happens if month january
    print(a)
    q = a.fiscal_quarter

    q_prev = q - 2
    print(q_prev)
    q_year = a.fiscal_year

    if q_prev == 0:
        q_prev = 4
        q_year -= 1

    q_year_str = str(q_year)
    print(q_prev, q_year_str)
    folders = []
    for month in quarter_months[q_prev - 1]:
        folders.append(q_year_str + month)

    print(folders)
    months[q_prev]

    return folders, q_year, months


if __name__ == "__main__":
    # file_one = open("demo.txt", "w")
    # file_one.write("first line of text\nsecond line of text\nthird line of text")
    # file_one.close()

    patrn = "FRDDMC61"
    result = check_quarter()

    i = 0

    for folder in result[0]:
        for day in range(monthrange(result[1], result[2][0][i])[1]):
            print(day+1)
            if day + 1 < 10:
                full_path = f'{PATH}{folder}/{folder}0{str(day+1)}_INTF.EPD'

                print(full_path+"\n")
            else:
                full_path = f'{PATH}{folder}/{folder}{str(day+1)}_INTF.EPD'

                print(full_path+"\n")
        i += 1