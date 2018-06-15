import json
from lxml import html
import requests

page = requests.get('https://www.fifa.com/worldcup/archive/switzerland1954/awards/index.html')
tree = html.fromstring(page.content)
world_cups = tree.xpath('//option/@value')

print(world_cups)
with open('tournaments.txt', 'w') as outfile:
    json.dump(world_cups, outfile)