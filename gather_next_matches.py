import re
import json
from lxml import html
import requests

def gather_matches(link):
    print('Parse: ' + link)
    page = requests.get(link)
    tree = html.fromstring(page.content)
    results = tree.find_class('fixture')
    for result in results:
        date = result.find_class('fi__info__datetime--abbr')
        teams = result.find_class('fi-t__nText')
        home = re.sub(' ', '_', teams[0].text_content())
        away = re.sub(' ', '_', teams[1].text_content())
        print('playMatch(\'' + date[0].text_content().strip() + '\', ' + home + ', ' + away + '),')

gather_matches('https://www.fifa.com/worldcup/matches/')