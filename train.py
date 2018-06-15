from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml.networkwriter import NetworkWriter
import json
import signal

run = True
def signal_handler(signal, frame):
    global run
    run = False
signal.signal(signal.SIGINT, signal_handler)

factor = 10.0
def normalize(score):
    return (score - factor / 2) / (factor / 2)

matches = []
with open('matches.txt') as f:
    matches = json.load(f)

teams = []
with open('teams.txt') as f:
    teams = json.load(f)

ds = SupervisedDataSet(len(teams), 2)
for match in matches:
    inputs = [0] * len(teams)
    inputs[teams.index(match['home'])] = 1
    inputs[teams.index(match['away'])] = -1
    if match['home_score'] > factor or match['away_score'] > factor:
        print('skip: ', match['home'], match['away'], match['home_score'], match['away_score'])
        continue
    outputs = [normalize(match['home_score']), normalize(match['away_score'])]
    ds.addSample(inputs, outputs)

net = buildNetwork(len(teams), len(teams), len(teams), 2)
trainer = BackpropTrainer(net, ds)

de = 1.0
error = 0.0
while run:
    tmp = error
    error = trainer.train()
    de = error - tmp
    print(error, de)

NetworkWriter.writeToFile(net, 'net.xml')