import csv
import fnmatch
import parsing
from parsing import cmpDates
import datetime

with open('personal_finance.csv', newline='') as csvfile:

    reader = csv.DictReader(csvfile)

    arguments = list(next(reader))
    print("\n\n")
    for i in arguments:
        print("    |    ", i, end="")
    print("\n\n")

    expression = input("    mask: ")
    expression = parsing.parseBlock(expression, arguments)


    res = 0
    print(expression)
    am = True if expression.find('amount') else False
    for row in reader:
        date = row['date']

        if eval(expression):
            if row['tag'] == 'investment' and row['location'] == "PAC":
                res += parsing.investValue(row)
            else:
                res += float(row['amount'])

print("\n\n    result = ", round(res,3))
print("\n\n")