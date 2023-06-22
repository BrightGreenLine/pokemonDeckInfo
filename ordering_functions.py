import requests

def get_secret_key():
    """Return the api key from the source. Temporarily, file on my drive"""
    with open('N:\\limitlessTCG\\ptcgio_apikey.txt', 'rt', encoding='UTF-8') as file:
        result = file.read()
    return result

def get_cards_from_set(setid):
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

    print("Cards found: " + str(len(cardslist)))
    return cardslist

def findbestprice(tcgplayerinfo):
    prices = tcgplayerinfo.get("prices")
    lowestprice = ['no rarity',99999999]
    for price in prices.keys():
        lowprice = prices[price]['low']
        if lowprice < lowestprice[1]:
            lowestprice[0] = price
            lowestprice[1] = prices[price]['low']

    return lowestprice

def createbuylist(cardlist, cardcounts, setcode):
    results=[]
    for card in cardlist:
        if card['price']<= 0.10:
            if cardcounts[card['name']] > 1:
                #Card has multiple printings, needs format of "{qty} {cardname} - {id}/{setsize} [{setid}]"
                results.append('4 ' + card['name'] + ' - ' + str(card['number']).zfill(3) + '/' + str(card['setsize']) + ' '+ setcode)
            else:
                #Card has single printings, needs format of "{qty} {cardname} [{setid}]"
                results.append('4 ' + card['name'] + ' ' + setcode + ' ' + str(card['number']).zfill(3) + '/' + str(card['setsize']))
    return results

def count_duplicates(cardlist):
    results={}
    for card in cardlist:
        name = card['name']
        if name not in results:
            results.update({name:1})
        else:
            results[name] +=1


    return results