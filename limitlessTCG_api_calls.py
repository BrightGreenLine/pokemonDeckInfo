import requests
from bs4 import BeautifulSoup as bs

def get_secret_key():
    """Return the api key from the source. Temporarily, file on my drive"""
    f = open('N:\\limitlessTCG\\apikey.txt', 'rt', encoding='UTF-8')
    result = f.read()
    return result

apikey = get_secret_key()

def get_tournament_data(apikey, from_date):
    headers = {'X-Access-Key' : apikey}
    try:
        formats = requests.get('https://play.limitlesstcg.com/api/games', headers=headers,timeout=5)
    except requests.ConnectTimeout:
        print("connection timed out")
    except requests.ConnectionError:
        print("failed to connect")
    except:
        print("Request failed for non-connect or timeout")
    
    print(formats.text)

get_tournament_data(apikey,0)