import re
import json
from lxml import html
import requests


def gather_matches(link):
    print('Parse: ' + link)
    page = requests.get(link)
    tree = html.fromstring(page.content)
    results = tree.find_class('result')
    matches = []
    for result in results:
        teams = result.find_class('t-nText')
        score = result.find_class('s-scoreText')
        re_result = re.search('(\d+)-(\d+)', score[0].text_content())
        if not re_result:
            continue
        matches.append({
            'home': teams[0].text_content().strip(),
            'away': teams[1].text_content().strip(),
            'home_score': int(re_result.group(1)),
            'away_score': int(re_result.group(2))
        })
    return matches


def gather_final_part(name):
    return gather_matches('https://www.fifa.com/worldcup/archive/' + name + '/matches/index.html')


def gather_quals(name):
    zones = ['europe', 'africa', 'asia', 'nccamerica', 'oceania', 'southamerica']
    matches = []
    for zone in zones:
        matches = matches + gather_matches('https://www.fifa.com/worldcup/archive/' + name +'/matches/preliminaries/' + zone + '/index.html')
    return matches

def gather_latest_quals():
    zones = ['europe', 'africa', 'asia', 'nccamerica', 'oceania', 'southamerica']
    matches = []
    for zone in zones:
        matches = matches + gather_matches('https://www.fifa.com/worldcup/preliminaries/' + zone + '/all-matches.html')
    return matches

def gather_full(name):
    return gather_quals(name) + gather_final_part(name)

matches = []
matches = matches + gather_latest_quals()
matches = matches + gather_full('brazil2014')
matches = matches + gather_full('southafrica2010')
matches = matches + gather_full('germany2006')
matches = matches + gather_full('koreajapan2002')
matches = matches + gather_full('france1998')
matches = matches + gather_full('usa1994')

print(len(matches), matches)
with open('matches.txt', 'w') as outfile:
    json.dump(matches, outfile)