#import limitlessTCG_parsing
import datetime
import limitlessTCG_api_calls as lapi

URL = "https://play.limitlesstcg.com/api/tournaments"
most_recent_tournament = datetime.datetime.fromisoformat('2023-04-03T00:00:00.000Z')
apikey = lapi.get_secret_key()

tournaments = lapi.get_tournament_data(apikey, URL, most_recent_tournament, 10)
new_tournaments = []

print("---------------")
print(tournaments)