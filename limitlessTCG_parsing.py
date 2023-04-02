import datetime
import requests
from bs4 import BeautifulSoup


"""
#until I figure out what I'm doing with classes, leave this out
class Tournament():
    def __init__(self, name, link):
        self.name = name
        self.link = None

class Participant():
    def __init__(self, id):
        self.id = id
"""

def get_new_tournaments_list(source_url, tournamentsAfterDate):
    """Grab only newer tournaments from LimitlessTCG, return a list of tournament objects"""
    base_url = source_url[:-1]
    pagenumber = 1
    requests_url = base_url + str(pagenumber)
    page = requests.get(requests_url, timeout=1)

    soup = BeautifulSoup(page.content, "html.parser")

    tournaments_list = soup.find(class_="striped completed-tournaments")
    
    tournaments = []
    tournaments.append(extract_tournament_information(tournaments_list))
    return tournaments

def extract_tournament_information(tournaments):
    """Get the high level information about a tournament, such as URL, player counts, winners"""
    rows = tournaments.find_all("tr")
    headers = {}
    head = tournaments.find_all("th")
    #print(head)
    if head:
        for column_position in range(len(head)):
            column_name = head[column_position]['data-sort'].strip().lower()
            headers[column_name] = column_position

    #sanitycheck = {0:'highlight', 1:'date', 2:'name', 3:'organizer', 4:'format', 5:'players', 6:'winner', 7:'tournamentURL'}

    #print("Headers:" + str(headers))
    #print(sanitycheck)

    #if(headers==sanitycheck):
    #    print("Headers haven't changed")

    i=len(headers)

    tournament_list = []

    for row in rows:
        tournament_info = extract_tournament_info_from_row(row, headers)
        if tournament_info is None:
            print('failed')
        else:
            tournament_list.append(tournament_info)

    return tournament_list


def extract_tournament_info_from_row(row, headers):
    """Use the header list to find each column if they move and create a dict for the tournament"""
    cells = row.find_all("td")
    tournament = {}
    if len(cells)==0:
        return tournament
    else:
        if len(cells[headers['highlight']].text)>0:
            highlighted = True
        else:
            highlighted = False

        tournament['timestamp'] = int(cells[headers['date']].a['data-time'])
        tournament['date'] = datetime.datetime.fromtimestamp(tournament['timestamp']/1000).isoformat()
        tournament['name'] = cells[headers['name']].text.strip()
        tournament['url'] = cells[headers['name']].a['href']
        tournament['organizer_name'] = cells[headers['organizer']].text.strip()
        tournament['organizer_url'] = cells[headers['organizer']].a['href']
        tournament['format'] = cells[headers['format']].img['data-tooltip'].lower()
        tournament['entrant_count'] = cells[headers['players']].text
        tournament['winner'] = cells[headers['winner']].text
    return tournament

def get_player_info_from_tournament(url):
    """Return a dict of the players in each tournament, and their w/l statistics"""
    page = requests.get(url, timeout=1)

    soup = BeautifulSoup(page.content, "html.parser")
