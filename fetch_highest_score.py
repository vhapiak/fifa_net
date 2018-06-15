import json

with open('matches.txt') as f:
    matches = json.load(f)

score = 0
for match in matches:
    home_score = int(match['home_score'])
    away_score = int(match['away_score'])
    score = max(score, home_score, away_score)

print(score)