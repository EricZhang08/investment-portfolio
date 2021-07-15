from requests_html import HTMLSession
import datetime
from datetime import timezone
from bs4 import BeautifulSoup

def get_html(company_code):
    session = HTMLSession()
    dt = datetime.datetime.today()
    dt = dt.replace(minute=00, hour=00, second=00)
    timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
    five_year_before = timestamp - 60 * 60 *24 *365 * 5 - 60 * 60 *24

    url =  'https://finance.yahoo.com/quote/'+company_code+'/history?period1='+ str(five_year_before) +  '&period2=' + str(timestamp) + '&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true'

    page = session.get(url)
    page.html.render()
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find( "table", {"data-test":"historical-prices"} )
    adj_close = list()
    for row in table.tbody.findAll("tr"):
        temp = row.findAll('td')
        if (len(temp)>6):
            adj_close.append(temp[5].text)
    return adj_close


print(get_html('APC.DE')[1])