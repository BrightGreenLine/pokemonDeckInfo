import ordering_functions as of

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

def sanitize_cardlist(cardlist):
    return 0

for inputcard in inputcards:
    card = {}
    bestprice = of.findbestprice(inputcard['tcgplayer'])
    card['name'] = inputcard['name']
    card['buyname'] = inputcard['name'].replace('é','e')
    card['id'] = inputcard['id']
    card['set'] = inputcard['set']['id']
    card['setsize'] = str(inputcard['set']['printedTotal'])
    card['number'] = str(int(inputcard['number'])).zfill(3)
    card['treatment'] = bestprice[0]
    card['price'] = float(bestprice[1])
    cardlist.append(separator.join([card['name'],card['id'],card['set'],str(card['number']),card['treatment'],str(card['price'])]))
    if(float(bestprice[1]) <= 0.05 and int(inputcard['number'])<=198): 
        buylist.append('4 ' + card['buyname'] + ' - ' + str(card['number']) + '/'+ card['setsize'] + ' ' + setcode)
    cards.append(card)
#Stop here and put this into my database

cardcounts = of.count_duplicates(cards)

newbuylist = of.createbuylist(cards, cardcounts, setcode)

print(cardlist)

with open("N:\\limitlessTCG\\cardlistings\\cards.csv",'w', encoding='UTF-8') as outputfile:
    for line in cardlist:
        outputfile.write(''.join(line))
        outputfile.write('\n')

with open("N:\\limitlessTCG\\cardlistings\\buylist.txt",'w', encoding='UTF-8') as buyfile:
    for line in newbuylist:
        buyfile.write(''.join(line))
        buyfile.write('\n')
