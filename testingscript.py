import limitlessTCG_parsing
#import pandas

URL = "https://play.limitlesstcg.com/tournaments/completed?game=PTCG&format=STANDARD&platform=PTCGL%2CPTCGO&type=all&time=all&page=1"

tournaments = limitlessTCG_parsing.get_new_tournaments_list(URL,0)
