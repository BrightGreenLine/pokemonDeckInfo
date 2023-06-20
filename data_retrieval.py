import requests
import re
import psycopg2 as postgres


def get_secret_key():
    """Return the api key from the source. Temporarily, file on my drive"""
    with open('N:\\limitlessTCG\\ptcgio_apikey.txt', 'rt', encoding='UTF-8') as file:
        result = file.read()
    return result



def get_cards_DSN():
    """Return the api key from the source. Temporarily, file on my drive"""
    with open('N:\\limitlessTCG\\cardDB.txt', 'rt', encoding='UTF-8') as file:
        result = file.read()  
    return result


def retrieve_setdata(setid):
    print(setid)
    dirty_cardlist = get_cards_from_api(setid)
    cards = sanitize_card_data(dirty_cardlist)
    return cards



def load_cards_to_database(cards):
    dsn = get_cards_DSN()
    dbconn = postgres.connect(dsn)
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
    cursor.execute("""DROP TABLE IF EXISTS public.card_list;
                CREATE TABLE public.card_list
                (  id integer generated always as identity,
                    card_name character varying COLLATE pg_catalog.\"default\" NOT NULL,
                    card_id character varying COLLATE pg_catalog.\"default\" NOT NULL,
                    buyname character varying COLLATE pg_catalog.\"default\" NOT NULL,
                    set_id character varying  COLLATE pg_catalog.\"default\" NOT NULL,
                    card_number integer NOT NULL,
                    card_setsize integer NOT NULL,
                    price decimal NOT NULL,
                    treatment character varying  COLLATE pg_catalog.\"default\" NOT NULL,
                    CONSTRAINT card_list_pkey PRIMARY KEY (card_id, id))
                TABLESPACE pg_default;
                ALTER TABLE public.card_list
                    OWNER to pokemon_data_agent;""")
    dbconn.commit()
    cursor.close()
    return



def insert_card_to_database(card, cursor):
    query = """insert into public.card_list
    (card_name, card_id, buyname, set_id, card_number, card_setsize, price, treatment)
	values 
    (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    """.format(cardname=card['name'],
               cardid=card['id'],
               buyname=card['buyname'],
               setid=card['set'],
               cardnumber=card['number'],
               setsize=card['setsize'],
               price=card['price'],
               treatment=card['treatment'])"""
    cursor.execute(query, (card['name'],
                           card['id'],
                           card['buyname'],
                           card['set'],
                           card['number'],
                           card['setsize'],
                           card['price'],
                           card['treatment']))
    return



def format_buyname(card):
    buyname = card['name'].replace('é','e')
    matches = re.split(r"([\s\w\']+)( \([\w\s\']+\)?)",buyname)
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

        query = response.json()
        for card in query['data']:
            cardslist.append(card)
        if query['count'] == query['pageSize']:
            page +=1
        else:
            read_complete=True

    print("Cards found: " + str(len(cardslist)) + " " + cardslist[0]['set']['id'])
    return cardslist