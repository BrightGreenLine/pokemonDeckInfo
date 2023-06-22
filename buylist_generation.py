import psycopg2 as pg
from psycopg2.extras import execute_values


def get_cards_DSN():
    """Return the api key from the source. Temporarily, file on my drive"""
    with open('N:\\limitlessTCG\\cardDB.txt', 'rt', encoding='UTF-8') as file:
        result = file.read()  
    return result



def generate_buylist(sets,price):
    cards = get_cardlist_from_database(sets)
    filtered_list = filter_cardlist_by_price(cards,price)
    text_buylist = create_buylist(filtered_list)
    return text_buylist



def get_cardlist_from_database(sets):
    dsn = get_cards_DSN()
    dbconn = pg.connect(dsn)
    splitsets = sets.split(',')
    query = """SELECT buyname, set_id, card_fullnumber, multiple_printings, price from( 
	select buyname,
	set_id,
	card_number,
	card_setsize,
	to_char(card_number, 'fm000')||'/'||to_char(card_setsize, 'fm000') as card_fullnumber,
	price,
	CASE
		WHEN 
			count(card_number) over (partition by card_name, set_id)=1
		THEN false
		else true
	end multiple_printings
	FROM public.card_list
	where set_id in %s) as iq"""
    cursor = dbconn.cursor(cursor_factory=pg.extras.NamedTupleCursor)
    execute_values(cursor, query, (splitsets,))
    #cursor.execute(query,(splitsets,price,))
    results = cursor.fetchall()
    for record in cursor:
        print(record)
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



def filter_cardlist_by_price(cardlist, price):
    new_cardlist = []
    for card in cardlist:
        if float(card.price)<=float(price):
            new_cardlist.append(card)
    return new_cardlist



def create_buylist(cards):
    output_list = []
    for card in cards:
        output_list.append(format_for_buylist(card))
    
    string_buylist = '\n'.join(output_list)
    return string_buylist



def format_for_buylist(card):
    if card.multiple_printings==True:                
        #Card has multiple printings, needs format of "{qty} {cardname} - {id}/{setsize} [{setid}]"
        result = f"4 {card.buyname} - {card.card_fullnumber} [{card.set_id}]"
    else:
        #Card has single printings, needs format of "{qty} {cardname} [{setid}] {cardnumber}"
        result = f"4 {card.buyname} [{card.set_id}] {card.card_fullnumber}"
    return result