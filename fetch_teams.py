import json

matches = []
with open('matches.txt') as f:
    matches = json.load(f)

teams = set()
for match in matches:
    teams.add(match['home'])
    teams.add(match['away'])

print(len(teams), teams)
with open('teams.txt', 'w') as outfile:
    json.dump(list(teams), outfile)