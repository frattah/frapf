import pandas as pd
import fnmatch
import parsing
import re

def doQuery(query, reader):
    """
        Perform the query passed by argument
    """
    res = 0
    for i, row in reader.iterrows():
        if eval(query):
            if row['tag'] == 'security' and float(row['amount']) > 0:
                res += parsing.investValue(row)
            else:
                res += float(row['amount'])
    return round(res,3)

def start(query):
    reader = pd.read_csv('personal_finance.csv', delimiter=',')
    # User Interface
    arguments = list(reader.columns)

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
