import argparse
from datetime import datetime
import data_retrieval
import buylist_generation

def main():
    args = getargs()
    
    match args.action:
        case 'refresh_data':
            refresh_database(args.set)
        case 'get_buylist':
            get_buylist(args.set, args.price)

    return



def getargs():
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-a', '--action',
                            choices=['get_buylist','refresh_data'],
                            required=True,
                            help='Get a buylist of cards for TCGPlayer or refresh the local price and card database')
    argParser.add_argument('-s', '--set',
                            required=True,
                            help='List of the set codes from api.pokemontcg.io/v2/sets.\n'+
                            'Required for refresh_data and get_buylist.\n'+
                            'Example: sv1,sv2')
    argParser.add_argument('-p','--price',
                           help="""The maximum price to use for building a buylist. \n
                           Example: 1.00 will return all cards costing 1.00 USD or less""")
    args = argParser.parse_args()
    return args



def refresh_database(string_sets):
    sets_to_retrieve = string_sets.split(",")
    cards = []
    print(f"{datetime.now()} | MESSAGE | Received request to retrieve the following sets: {string_sets}")
    for setlist in sets_to_retrieve:
        new_cardlist = data_retrieval.retrieve_setdata(setlist)
        for card in new_cardlist:
            cards.append(card)
    
    if len(cards)==0:
        print(f"{datetime.now()} | MESSAGE | No cards retrieved from pokemontcg.io API")
        return
    print(f"{datetime.now()} | MESSAGE | {len(cards)} cards retrieved from pokemontcg.io API")

    data_retrieval.load_cards_to_database(cards)
    return



def get_buylist(sets, price):
    timestamp = datetime.now()
    print(f"{timestamp} || Requesting buylist for {sets} under ${price}")
    cardlist = buylist_generation.generate_buylist(sets, price)
    print(cardlist)
    return



if __name__ == "__main__":
    main()