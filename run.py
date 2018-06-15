
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

home = sys.argv[2]
away = sys.argv[3]
inputs = [0] * len(teams)

inputs[teams.index(home)] = 1
inputs[teams.index(away)] = -1
result = net.activate(inputs)
result[0] = unnormalize(result[0])
result[1] = unnormalize(result[1])
print('Home:', home, away, result[0], result[1])

total = result

inputs[teams.index(home)] = -1
inputs[teams.index(away)] = 1
result = net.activate(inputs)
result[0] = unnormalize(result[0])
result[1] = unnormalize(result[1])
print('Away:', away, home, result[0], result[1])

total[0] = total[0] + result[1]
total[1] = total[1] + result[0]
print('Total:', home, away, total[0] / 2, total[1] / 2)