import argparse
from datetime import datetime
from flask import Flask, request, make_response, jsonify
import os
from dotenv import load_dotenv
import data_retrieval
import buylist_generation

load_dotenv()

app = Flask(__name__)

"""
@app.route("/", methods=['GET'])
def get_responses():
    print(request.query_string)
    print(f"Action is: {request.args.get('action')}")
    print(f"Setlists are: {request.args.get('sets')}")
    print(f"Price is: {request.args.get('price')}")
    
    match request.args.get('action'):
        case 'refresh_data':
            refresh_database(request.args.get('sets'))
            display = f"{datetime.now()} hahaha nope"
        case 'get_buylist':
            display = get_buylist(request.args.get('sets'), request.args.get('price'))
    
    response = make_response(display, 200)
    response.mimetype = "text/plain"
    return response"""




@app.route("/buylist/")
def make_buylist():
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if True: #data_retrieval.validate_credentials(auth):
        display = get_buylist(request.args.get('sets'), request.args.get('price'))
    
        response = make_response(display, 200)
        response.mimetype = "text/plain"
        return response
    else: #placeholder for if auth is required
        return jsonify({"message": "ERROR: Unauthorized"}),401

@app.route("/refreshdata/", methods=['POST'])
def refresh_carddata():
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if data_retrieval.validate_credentials(auth):
        refresh_database('sv1,sv2,swsh11')
        return jsonify({"message":"OK: Authorized"}), 200
    else:
        return jsonify({"message": "ERROR: Unauthorized"}),401
    return

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
        if new_cardlist is None:
            print(f"{datetime.now()} | ERROR | Failed to retrieve cards from API")
            return
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
    return cardlist



if __name__ == "__main__":
    #main()
    print(f"Secret key is:{os.getenv('SECRETS_PATH')}")
    app.run(host='0.0.0.0', port=6969)