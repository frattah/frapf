import re
import keyword
import globals
import requests
from bs4 import BeautifulSoup

def cmpDates(date1, date2):
    """
        Return True if date1 is before date2 or they are equals
    """
    date1 = date1.split('-')
    date2 = date2.split('-')
    if date1[0] == date2[0]:
        if date1[1] == date2[1]:
            return date1[2] == '??' or date1[2] <= date2[2] or date2[2] == '??'
        else:
            return date1[1] <= date2[1]
    else:
        return date1[0] <= date2[0]
    
def parseRangeDates(expression):
    """
        Replace all range dates like ****-**-** | ****-**-** using the cmpDates() function
    """
    
    patt = 0
    
    while patt != None:

        patt = re.search(globals.DATE_PATTERN + '[ ]*[|]{1}[ ]*' + globals.DATE_PATTERN, expression, patt.end() if patt != 0 else 0)
        if patt != None:
            tmp = patt.group()
            tmp = tmp.split()
            expression = expression.replace(tmp[0], "cmpDates('" + tmp[0] + "',row['date'])")
            expression = expression.replace(tmp[1], " and ", 1)
            expression = expression.replace(tmp[2], "cmpDates(row['date'],'" + tmp[2] + "')")
    return expression

def parseBlock(expression, arguments):
    """
        Prepare the expression to the final evaluation replacing specific statements with python's builtin
    """
    
    # Split operators with spaces
    for i in globals.OPERATORS:
        expression = expression.replace(i, i + ' ')

    expression = parseRangeDates(expression)

    tmp = expression.split()
    for i in range(0, len(tmp)):

        if tmp[i].lower() in arguments:
            tmp[i] = "row['" + tmp[i].lower() + "']"

        elif re.match(globals.DATE_PATTERN, tmp[i]):
            tmp[i] = "fnmatch.fnmatch(row['date'], '" + str(tmp[i]) + "')"

        elif tmp[i].upper() == "NULL":
            tmp[i] = "'NULL'"
        
        elif not(keyword.iskeyword(tmp[i])) and tmp[i] not in globals.OPERATORS and tmp[i][:9] != "cmpDates(":
            tmp[i] = "'" + tmp[i] + "'"

        tmp[i] = ' ' + tmp[i]

    return ''.join(tmp)


def investValue(row):
    """
        Return the real-time value of the stocks passed by argument
    """

    # Get from the database informations that you need
    investment_info = row['reason'].split(':')
    ticker = investment_info[0]
    market = investment_info[1]
    stocks_number = investment_info[2]

    # Access to google finance
    try:
        price = globals.tickers[ticker]
        print(price)
    except KeyError:
        url = f"{globals.GOOGLE_FINANCE_URL}/quote/{ticker}:{market}?hl=en"
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        items = soup.find_all("div", {"class": "AHmHk"})
        price = items[0].find("div", {"class": "YMlKec fxKbKc"}).text
        price = price[1:]
        globals.tickers[ticker] = price

    return float(price) * int(stocks_number)