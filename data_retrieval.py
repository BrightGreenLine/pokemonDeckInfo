import re
from datetime import datetime
import requests
import psycopg2 as pg
import os, os.path
from dotenv import load_dotenv

load_dotenv()

def get_secret_key():
    """Return the api key from the source. Temporarily, file on my drive"""
    with open(os.path.join(os.getenv('SECRETS_PATH'),"ptcgio_apikey.txt"), "rt", encoding='UTF-8') as file:
        result = file.read()
    return result



def get_cards_DSN():
    """Return the api key from the source. Temporarily, file on my drive"""
    with open(os.path.join(os.getenv('SECRETS_PATH'),"cardDB.txt"), "rt", encoding='UTF-8') as file:
        result = file.read()  
    return result



def retrieve_setdata(setid):
    dirty_cardlist = get_cards_from_api(setid)
    if (dirty_cardlist is None) or (len(dirty_cardlist) == 0):
        return None
    cards = sanitize_card_data(dirty_cardlist)
    return cards



def load_cards_to_database(cards):
    dsn = get_cards_DSN()
    dbconn = pg.connect(dsn)
    drop_and_recreate_cards_table(dbconn)

    cursor = dbconn.cursor()
    for card in cards:
        insert_card_to_database(card, cursor)
    dbconn.commit()
    cursor.close()
    dbconn.close()
    return



def drop_and_recreate_cards_table(dbconn):
    cursor = dbconn.cursor()
    cursor.execute("""CALL public.drop_and_refresh_table()""")
    dbconn.commit()
    cursor.close()
    return



def insert_card_to_database(card, cursor):
    query = """insert into public.card_list
    (card_name, card_id, buyname, set_id, rarity, card_number, card_setsize, price, treatment)
	values 
    (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query, (card['name'],
                           card['id'],
                           card['buyname'],
                           card['set'],
                           card['rarity'],
                           card['number'],
                           card['setsize'],
                           card['price'],
                           card['treatment']))
    return



def format_buyname(card):
    buyname = card['name'].replace('é','e')
    matches = re.split(r"([\s\w\'\’]+)( \([\w\s\']+\)?)",buyname)
    if len(matches) ==1:
        buyname = matches[0]
    else:
        buyname = matches[1]
    return buyname



def sanitize_card_data(raw_cardlist):
    """Extract all the card info, clean up names and flatten
    the hierarchy from the pokemon tcg api"""
    cards = []
    for inputcard in raw_cardlist:
        card = {}
        bestprice = findbestprice(inputcard['tcgplayer'])
        card['name'] = inputcard['name']
        card['rarity'] = inputcard['rarity']
        card['buyname'] = format_buyname(card)
        card['id'] = inputcard['id']
        card['set'] = inputcard['set']['id']
        card['setsize'] = int(inputcard['set']['printedTotal'])
        card['number'] = int(inputcard['number'])
        card['treatment'] = bestprice[0]
        card['price'] = float(bestprice[1])
        cards.append(card)

    return cards



def findbestprice(tcgplayerinfo):
    prices = tcgplayerinfo.get("prices")
    lowestprice = ['no rarity',99999999]
    for price in prices.keys():
        lowprice = prices[price]['low']
        if lowprice < lowestprice[1]:
            lowestprice[0] = price
            lowestprice[1] = prices[price]['low']

    return lowestprice



def get_cards_from_api(setid):
    cardslist = []
    page = 1
    read_complete = False
    apikey = get_secret_key()
    pokemonapi = "https://api.pokemontcg.io/v2/cards"
    headers = {'X-Api-Key': apikey}
    while read_complete==False:
        payload = {'q':'set.id:'+ setid,'select':'name,tcgplayer,number,rarity,set,id,subtypes,supertypes','orderBy':'number','page':page}
        #response = requests.get(pokemonapi, headers=headers,timeout=15)
        try:
            response = requests.get(pokemonapi, headers=headers,timeout=60,params=payload)
            #print("response collected")
        except requests.ConnectTimeout:
            print("connection timed out")
        except requests.ConnectionError:
            print("failed to connect")
        except:
            print("Request failed for non-connect or timeout")

        if response.status_code != 200:
            print(f"{datetime.now()} | ERROR | Response received from api was not okay: {response.status_code}")
            return None

        query = response.json()
        for card in query['data']:
            cardslist.append(card)
        if query['count'] == query['pageSize']:
            page +=1
        else:
            read_complete=True

    return cardslist



def validate_credentials(auth):
    dsn = get_cards_DSN()
    dbconn = pg.connect(dsn)
    cursor = dbconn.cursor()

    cursor.execute("""SELECT keyvalue from user_keys where keyvalue = %s""", (auth,))
    results = cursor.fetchall()
    if len(results) > 0:
        return True
    return False