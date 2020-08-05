import requests
from bs4 import BeautifulSoup


class Race:

    def __init__(self, group, office):
        self.group = group
        self.office = office
        self.candidates = []

    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def __str__(self):
        return "{self.office}".format(self=self)


class Candidate:

    def __init__(self, name, election, party, votes):
        self.name = name
        self.election = election
        self.party = party
        self.votes = votes


executive_races = ["Governor", "Lt. Governor", "Secretary of State", "State Treasurer", "State Auditor", "Attorney General", "Commissioner of Public Lands", "Superintendent of Public Instruction", "Insurance Commissioner"]
legislative_races = ["Congressional District 4 - U.S. Representative", "LEGISLATIVE DISTRICT 13 - State Representative Pos. 1", "LEGISLATIVE DISTRICT 13 - State Representative Pos. 2", "Legislative District 14 - State Representative Pos. 1", "Legislative District 15 - Representative, Position 1", "Legislative District 15 - Representative, Position 2",  ]

results_feed = requests.get("https://results.vote.wa.gov/results/current/export/20200804_AllState.xml")
results_content = results_feed.text
soup = BeautifulSoup(results_content, 'xml')

for race in executive_races:
    Race('executive', race)









