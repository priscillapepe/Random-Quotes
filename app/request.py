import requests,json
# from .models import Quote

url = "http://quotes.stormconsultancy.co.uk/random.json"

def get_quotes():
    '''
    Function to consume http request and return a Quote class instance 
    '''

    response = requests.get(url).json()
    return response