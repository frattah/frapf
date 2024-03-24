import csv
import fnmatch
import parsing
import re
from currency_converter import CurrencyConverter

def doQuery(query, reader):
    """
        Perform the query passed by argument
    """
    res = 0
    for row in reader:
        if eval(query):
            if row['tag'] == 'investment' and row['location'] == "PAC":
                res += parsing.investValue(row)
            else:
                res += float(row['amount'])
    return round(res,3)

def main():
    with open('personal_finance.csv', newline='') as csvfile:
        # Csv opening
        reader = csv.DictReader(csvfile)

        # Currency convertion support
        converter = CurrencyConverter()

        # User Interface
        arguments = list(next(reader))
        print("\n\n")
        for i in arguments:
            print("    |    ", i, end="")
        print("\n\n")
        query = input("    query: ")

        currency = 'EUR'
        match = re.search(r"in[ ]*[a-zA-Z]{3}", query)
        if match != None:
            currency = match.group()[-3:]
            query = query.replace(match.group(), "")

        # query parsing
        query = parsing.parseBlock(query, arguments)

        result = doQuery(query, reader)
        result = round(converter.convert(result, 'EUR', currency), 2)

        print(query)
        print("\n\n    result = ", result, " ", currency)
        print("\n\n")

if __name__ == '__main__':
    main()
