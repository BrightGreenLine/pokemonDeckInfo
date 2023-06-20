import argparse
import ordering_functions as of
import data_retrieval as dr

def main():
    args = getargs()
    
    match args.action:
        case 'refresh_data':
            refresh_database(args.set)
        case 'get_buylist':
            get_buylist(args.set)

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
    args = argParser.parse_args()
    return args

def refresh_database(string_sets):
    sets_to_retrieve = string_sets.split(",")
    cards = []
    print(sets_to_retrieve)
    for set in sets_to_retrieve:
        new_cardlist = dr.retrieve_setdata(set)
        for card in new_cardlist:
            cards.append(card)
    
    if len(cards)==0:
        return
    else:
        dr.load_cards_to_database(cards)
    return

def get_buylist(sets):
    print(sets)
    return

if __name__ == "__main__":
    main()