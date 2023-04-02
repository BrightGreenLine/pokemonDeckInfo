import tournaments
#import pandas

URL = "https://play.limitlesstcg.com/tournaments/completed?game=PTCG&format=STANDARD&platform=PTCGL%2CPTCGO&type=all&time=all&page=1"

events_list = tournaments.get_new_tournaments_list(URL,0)
tournament_list = tournaments.extract_tournament_information(events_list)

print(tournament_list)

#print(headers)
#print(tournamentsList)
