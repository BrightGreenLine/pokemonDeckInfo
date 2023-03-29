import tournaments
#import pandas

URL = "https://play.limitlesstcg.com/tournaments/completed?game=PTCG&format=STANDARD&platform=PTCGL%2CPTCGO&type=all&time=all&page=1"

tournamentlist = tournaments.get_new_tournaments_list(URL,0)
tournaments.extract_tournament_information(tournamentlist)

#print(headers)
#print(tournamentsList)
