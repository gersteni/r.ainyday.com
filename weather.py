from google.appengine.api import urlfetch
from xml.dom import minidom

# at this moment, returns just the plain text forecast. This will need to factor in
# current time in the location, and we may end up neededing more data than just the plain
# text
def zipcode_fetch(zip_str):
    result = urlfetch.fetch("http://www.google.com/ig/api?weather=" + zip_str)
    if result.status_code == 200:
        dom = minidom.parseString(result.content)
        forecasts = dom.getElementsByTagName("forecast_conditions")
        if len(forecasts) > 0:
            condition = forecasts[0].getElementsByTagName("condition")[0]
            forecast = condition.getAttribute("data")
            return forecast

def is_rain(forecast):
    return forecast != "Clear"
