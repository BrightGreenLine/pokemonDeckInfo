"""All the functions for interfacing with the LimitlessTCG API"""
import requests
import datetime

def get_secret_key():
    """Return the api key from the source. Temporarily, file on my drive"""
    with open('N:\\limitlessTCG\\apikey.txt', 'rt', encoding='UTF-8') as file:
        result = file.read()
    return result

def get_tournament_data(apikey, url, from_date, limit):
    headers = {'X-Access-Key' : apikey}
    payload = {'game':'PTCG','format':'STANDARD','limit':limit}
    try:
        response = requests.get(url, headers=headers,timeout=5,params=payload)
    except requests.ConnectTimeout:
        print("connection timed out")
    except requests.ConnectionError:
        print("failed to connect")
    except:
        print("Request failed for non-connect or timeout")

    tournament_list = response.json()
    results = fix_tournament_data_types(tournament_list)
    found_all_new_tournaments = False

    for tournament in results:
        if tournament['date'] < from_date:
            found_all_new_tournaments = True
    
    if found_all_new_tournaments == False:
        results = get_tournament_data(apikey, url, from_date, limit + 10)

    return results

def fix_tournament_data_types(tournaments):
    for tournament in tournaments:
        if type(tournament['date'])==str:
            tournament['date']=datetime.datetime.fromisoformat(tournament['date'])
    return tournaments