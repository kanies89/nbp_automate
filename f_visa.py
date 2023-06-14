from calendar import monthrange
from fiscalyear import FiscalDate

PATH = "./visa_data/"
# PATH = "\\\\prdfil\\tf$\\Internal\\clearing\\Visa\\"

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


matched_lines = []  # List to store the matched lines


def grep(path):
    pattern = 'FRDDMC61'  # Replace with your desired pattern

    with open(path, 'r') as file:
        file = file.readlines()
        for lines in file:
            if pattern in lines:
                if '******' in lines:
                    matched_lines.append(lines)


def find():
    result = check_quarter()

    i = 0

    for folder in result[0]:
        for day in range(monthrange(result[1], result[2][0][i])[1]):
            if day + 1 < 10:
                full_path = f'{PATH}{folder}/{folder}0{str(day + 1)}_INITF.EPD'
                print(full_path)
                grep(full_path)
            else:
                full_path = f'{PATH}{folder}/{folder}{str(day + 1)}_INITF.EPD'
                print(full_path)
                grep(full_path)
        i += 1

    for line in matched_lines:
        print(line)


if __name__ == "__main__":
    find()
    for d in matched_lines:
        print(len(d))
