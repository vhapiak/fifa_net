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
        self.matches = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

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


class Match:
    def __init__(self, date, home, away, home_score, away_score, winner, loser):
        self.date = date
        self.home = home
        self.away = away
        self.home_score = home_score
        self.away_score = away_score
        self.winner = winner
        self.loser = loser

    def __str__(self):
        return str(self.home) + ' ' + str(self.home_score) + '-' + str(self.away_score) + ' ' + str(self.away) + ' : ' + str(self.winner)

    def __repr__(self):
        return self.__str__()

def playMatch(date, home, away):
    inputs = [0] * len(teams)
    inputs[home.id] = 1
    inputs[away.id] = -1
    result = net.activate(inputs)
    result[0] = unnormalize(result[0])
    result[1] = unnormalize(result[1])

    total = result

    inputs[home.id] = -1
    inputs[away.id] = 1
    result = net.activate(inputs)
    result[0] = unnormalize(result[0])
    result[1] = unnormalize(result[1])

    total[0] = (total[0] + result[1]) / 2
    total[1] = (total[1] + result[0]) / 2

    winner = None
    loser = None
    if total[0] > total[1]:
        winner = home
        loser = away
    else:
        winner = away
        loser = home
    match = Match(date, home, away, round(total[0]), round(total[1]), winner, loser)
    home.matches.append(match)
    away.matches.append(match)
    return match

group_round = [
    playMatch('14 Jun 2018', Russia, Saudi_Arabia),
    playMatch('15 Jun 2018', Egypt, Uruguay),
    playMatch('15 Jun 2018', Morocco, IR_Iran),
    playMatch('15 Jun 2018', Portugal, Spain),
    playMatch('16 Jun 2018', France, Australia),
    playMatch('16 Jun 2018', Argentina, Iceland),
    playMatch('16 Jun 2018', Peru, Denmark),
    playMatch('16 Jun 2018', Croatia, Nigeria),
    playMatch('17 Jun 2018', Costa_Rica, Serbia),
    playMatch('17 Jun 2018', Germany, Mexico),
    playMatch('17 Jun 2018', Brazil, Switzerland),
    playMatch('18 Jun 2018', Sweden, Korea_Republic),
    playMatch('18 Jun 2018', Belgium, Panama),
    playMatch('18 Jun 2018', Tunisia, England),
    playMatch('19 Jun 2018', Colombia, Japan),
    playMatch('19 Jun 2018', Poland, Senegal),
    playMatch('19 Jun 2018', Russia, Egypt),
    playMatch('20 Jun 2018', Portugal, Morocco),
    playMatch('20 Jun 2018', Uruguay, Saudi_Arabia),
    playMatch('20 Jun 2018', IR_Iran, Spain),
    playMatch('21 Jun 2018', Denmark, Australia),
    playMatch('21 Jun 2018', France, Peru),
    playMatch('21 Jun 2018', Argentina, Croatia),
    playMatch('22 Jun 2018', Brazil, Costa_Rica),
    playMatch('22 Jun 2018', Nigeria, Iceland),
    playMatch('22 Jun 2018', Serbia, Switzerland),
    playMatch('23 Jun 2018', Belgium, Tunisia),
    playMatch('23 Jun 2018', Korea_Republic, Mexico),
    playMatch('23 Jun 2018', Germany, Sweden),
    playMatch('24 Jun 2018', England, Panama),
    playMatch('24 Jun 2018', Japan, Senegal),
    playMatch('24 Jun 2018', Poland, Colombia),
    playMatch('25 Jun 2018', Uruguay, Russia),
    playMatch('25 Jun 2018', Saudi_Arabia, Egypt),
    playMatch('25 Jun 2018', Spain, Morocco),
    playMatch('25 Jun 2018', IR_Iran, Portugal),
    playMatch('26 Jun 2018', Australia, Peru),
    playMatch('26 Jun 2018', Denmark, France),
    playMatch('26 Jun 2018', Nigeria, Argentina),
    playMatch('26 Jun 2018', Iceland, Croatia),
    playMatch('27 Jun 2018', Korea_Republic, Germany),
    playMatch('27 Jun 2018', Mexico, Sweden),
    playMatch('27 Jun 2018', Serbia, Brazil),
    playMatch('27 Jun 2018', Switzerland, Costa_Rica),
    playMatch('28 Jun 2018', Japan, Poland),
    playMatch('28 Jun 2018', Senegal, Colombia),
    playMatch('28 Jun 2018', Panama, Tunisia),
    playMatch('28 Jun 2018', England, Belgium),
]

class GroupResult:
    def __init__(self, member):
        self.member = member
        self.matches = 0
        self.win = 0
        self.lose = 0
        self.draw = 0
        self.positive = 0
        self.negative = 0
        self.score = 0

class Group:
    def __init__(self, name, members):
        self.name = name
        self.results = []

        for member in members:
            result = GroupResult(member)
            for match in member.matches:
                is_home = True
                if match.away == member:
                    is_home = False
                if is_home:
                    result.positive = result.positive + match.home_score
                    result.negative = result.negative + match.away_score
                else:
                    result.positive = result.positive + match.away_score
                    result.negative = result.negative + match.home_score
                if match.home_score == match.away_score:
                    result.draw = result.draw + 1
                    result.score = result.score + 1
                else:
                    if match.winner == member:
                        result.win = result.win + 1
                        result.score = result.score + 3
                    else:
                        result.lose = result.lose + 1

            self.results.append(result)

        self.results.sort(key = lambda result: result.score, reverse=True)
        if self.results[1].score == self.results[2].score:
            print('Need help')
        self.winner = self.results[0].member
        self.second = self.results[1].member

GroupA = Group('A', [Russia, Saudi_Arabia, Egypt, Uruguay])
GroupB = Group('B', [IR_Iran, Portugal, Spain, Morocco])
GroupC = Group('C', [France, Australia, Peru, Denmark])
GroupD = Group('D', [Argentina, Iceland, Croatia, Nigeria])
GroupE = Group('E', [Brazil, Switzerland, Costa_Rica, Serbia])
GroupF = Group('F', [Germany, Mexico, Sweden, Korea_Republic])
GroupG = Group('G', [Belgium, Panama, Tunisia, England])
GroupH = Group('H', [Poland, Senegal, Colombia, Japan])

stage_of_16 = [
    playMatch('30 Jun 2018', GroupC.winner, GroupD.second),
    playMatch('30 Jun 2018', GroupA.winner, GroupB.second),
    playMatch('01 Jul 2018', GroupB.winner, GroupA.second),
    playMatch('01 Jul 2018', GroupD.winner, GroupC.second),
    playMatch('02 Jul 2018', GroupE.winner, GroupF.second),
    playMatch('02 Jul 2018', GroupG.winner, GroupH.second),
    playMatch('03 Jul 2018', GroupF.winner, GroupE.second),
    playMatch('03 Jul 2018', GroupH.winner, GroupG.second),
]

quater_final = [
    playMatch('06 Jul 2018', stage_of_16[1].winner, stage_of_16[0].winner),
    playMatch('06 Jul 2018', stage_of_16[4].winner, stage_of_16[5].winner),
    playMatch('07 Jul 2018', stage_of_16[6].winner, stage_of_16[7].winner),
    playMatch('07 Jul 2018', stage_of_16[2].winner, stage_of_16[3].winner),
]

semi_final = [
    playMatch('10 Jul 2018', quater_final[0].winner, quater_final[1].winner),
    playMatch('11 Jul 2018', quater_final[2].winner, quater_final[3].winner),
]

third_place = playMatch('14 Jul 2018', semi_final[0].loser, semi_final[1].loser)
final = playMatch('15 Jul 2018', semi_final[0].winner, semi_final[1].winner)

print (group_round)
print (stage_of_16)
print (quater_final)
print (semi_final)
print (third_place)
print (final)