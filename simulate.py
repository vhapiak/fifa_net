from pybrain.tools.customxml.networkreader import NetworkReader
import json
import sys

factor = 10.0
def unnormalize(score):
    return score * (factor / 2) + factor / 2

teams = []
with open('teams.txt') as f:
    teams = json.load(f)

net = NetworkReader.readFrom(sys.argv[1])

class Team:
    def __init__(self, name):
        self.name = name
        self.id = teams.index(name)
        self.matches = {}

Argentina = Team('Argentina')
Australia = Team('Australia')
Belgium = Team('Belgium')
Brazil = Team('Brazil')
Colombia = Team('Colombia')
Costa_Rica = Team('Costa Rica')
Croatia = Team('Croatia')
Denmark = Team('Denmark')
Egypt = Team('Egypt')
England = Team('England')
France = Team('France')
Germany = Team('Germany')
Iceland = Team('Iceland')
IR_Iran = Team('IR Iran')
Japan = Team('Japan')
Korea_Republic = Team('Korea Republic')
Mexico = Team('Mexico')
Morocco = Team('Morocco')
Nigeria = Team('Nigeria')
Panama = Team('Panama')
Peru = Team('Peru')
Poland = Team('Poland')
Portugal = Team('Portugal')
Russia = Team('Russia')
Saudi_Arabia = Team('Saudi Arabia')
Senegal = Team('Senegal')
Serbia = Team('Serbia')
Spain = Team('Spain')
Sweden = Team('Sweden')
Switzerland = Team('Switzerland')
Tunisia = Team('Tunisia')
Uruguay = Team('Uruguay')