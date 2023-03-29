import datetime
import requests
from bs4 import BeautifulSoup

def get_new_tournaments_list(source_url, tournamentsAfterDate):
    base_url = source_url[:-1]
    pagenumber = 1
    requests_url = base_url + str(pagenumber)
    page = requests.get(requests_url, timeout=1)

    soup = BeautifulSoup(page.content, "html.parser")

    tournaments_list = soup.find(class_="striped completed-tournaments")
    return(tournaments_list)

def extract_tournament_information(tournaments):
    rows = tournaments.find_all("tr")
    headers = {}
    head = tournaments.find_all("th")
    #print(head)
    if head:
        for i in range(len(head)):
            headers[i] = head[i]['data-sort'].strip().lower()

    sanitycheck = {0:'highlight', 1:'date', 2:'name', 3:'organizer', 4:'format', 5:'players', 6:'winner', 7:'tournamentURL'}

    #print("Headers:" + str(headers))
    #print(sanitycheck)

    #if(headers==sanitycheck):
    #    print("Headers haven't changed")

    i=len(headers)
    headers[i] = "tournamentURL"
    for row in rows:
        tournamentInfo = extractTournamentInfoFromRow(row, headers)
        if tournamentInfo==None:
            print('failed')
        else:
            print('Append the results here')


def extractTournamentInfoFromRow(row, headers):
    cells = row.find_all("td")
    if(len(cells)>0):
        if len(cells[0].text)>0:
            highlighted = True
        else:
            highlighted = False
        timestamp = int(cells[1].a['data-time'])
        date = datetime.datetime.fromtimestamp(timestamp/1000).isoformat()
        name = cells[2].text.strip()
        url = cells[2].a['href']
        organizer_name = cells[3].text.strip()
        #tournamentOrganizerUrl = cells[3].a['href']
        format = cells[4].img['data-tooltip'].lower()
        entrant_count = cells[5].text
        winner = cells[6].text
        print(name)
    return None