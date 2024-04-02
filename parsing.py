import keyword
import globals
import requests
from bs4 import BeautifulSoup

def parseBlock(expression, arguments):
    """
        Prepare the expression to the final evaluation replacing specific statements with python's builtin
    """
    
    # Split operators with spaces
    for i in globals.OPERATORS:
        expression = expression.replace(i, i + ' ')

    tmp = expression.split()
    for i in range(0, len(tmp)):

        # Expand arguments
        if tmp[i].lower() in arguments:
            tmp[i] = "row['" + tmp[i].lower() + "']"

        # Make string from non keyword and non operators words
        elif not(keyword.iskeyword(tmp[i])) and tmp[i] not in globals.OPERATORS and not(tmp[i].isdigit()):
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
    except KeyError:
        url = f"{globals.GOOGLE_FINANCE_URL}/quote/{ticker}:{market}?hl=en"
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        price = float(soup.find("div", class_="YMlKec fxKbKc").text[1:])
        globals.tickers[ticker] = price

    return float(price) * int(stocks_number)

def currencyConvertion(currency):
    """
        Given a currency code return the change from EUR
    """

    url = f"{globals.GOOGLE_FINANCE_URL}/quote/EUR-{currency}?hl=en"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    convertion = float(soup.find("div", class_="YMlKec fxKbKc").text.replace(",", ""))
    
    return convertion