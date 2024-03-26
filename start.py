import csv
import fnmatch
import parsing
import re

def doQuery(query, reader):
    """
        Perform the query passed by argument
    """
    res = 0
    for row in reader:
        if eval(query):
            if row['tag'] == 'investment' and float(row['amount']) > 0:
                res += parsing.investValue(row)
            else:
                res += float(row['amount'])
    return round(res,3)

def start(query):
    with open('personal_finance.csv', newline='') as csvfile:

        reader = csv.DictReader(csvfile)

        # User Interface
        arguments = list(next(reader))

        currency = 'EUR'
        match = re.search(r"in[ ]{1}[a-zA-Z]{3}", query)
        if match != None:
            currency = match.group()[-3:].upper()
            query = query.replace(match.group(), "")

        # query parsing
        query = parsing.parseBlock(query, arguments)
        result = doQuery(query, reader)

        if currency != 'EUR':
            result = round(result * parsing.currencyConvertion(currency), 2)

        print("\n\n    result = ", result, currency)
        print("\n\n")
