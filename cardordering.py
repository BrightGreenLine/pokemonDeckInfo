import argparse
import ordering_functions as of

argParser = argparse.ArgumentParser()
argParser.add_argument('-a', '--action',
                        choices=['get_buylist','refresh_data'],
                        required=True,
                        help='Get a buylist of cards for TCGPlayer or refresh the local price and card database')
args = argParser.parse_args()

inputcards = []
setcode = "[SV01]"

inputcards = of.get_cards_from_set('sv1')

#inputcards = jsondata['data']

headers = "name,id,set,cardnumber,treatment,price"
cardlist = []
cards = []
buylist = []
cardlist.append(headers)
separator = ","

def sanitize_cardlist(raw_cardlist):
    """Extract all the card info, clean up names and flatten
    the hierarchy from the pokemon tcg api"""
    cards = []
    for inputcard in raw_cardlist:
        card = {}
        bestprice = of.findbestprice(inputcard['tcgplayer'])
        card['name'] = inputcard['name']
        card['buyname'] = inputcard['name'].replace('é','e')
        card['id'] = inputcard['id']
        card['set'] = inputcard['set']['id']
        card['setsize'] = int(inputcard['set']['printedTotal'])
        card['number'] = int(inputcard['number'])
        card['treatment'] = bestprice[0]
        card['price'] = float(bestprice[1])
        cards.append(card)

    return cards

cardlist = sanitize_cardlist(inputcards)

#Stop here and put this into my database

cardcounts = of.count_duplicates(cardlist)

newbuylist = of.createbuylist(cardlist, cardcounts, setcode)

print(cardlist)

with open("N:\\limitlessTCG\\cardlistings\\cards.csv",'w', encoding='UTF-8') as outputfile:
    for card in cardlist:
        line = ",".join([card['name'],card['id'],card['set'],str(card['number'])])
        outputfile.write(line + '\n')

with open("N:\\limitlessTCG\\cardlistings\\buylist.txt",'w', encoding='UTF-8') as buyfile:
    for line in newbuylist:
        buyfile.write(''.join(line))
        buyfile.write('\n')
