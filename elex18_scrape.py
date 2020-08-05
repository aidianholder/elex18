from bs4 import BeautifulSoup
import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
url = "https://results.vote.wa.gov/results/current/export/20200804_AllState.xml"
r = requests.get(url, headers=headers)
content = r.text
soup = BeautifulSoup(content, 'xml')


"""def lookup_party(party_string):
    party_lookup = {"(Prefers Republican Party)": "Republican", "(Prefers Democratic Party)": "Democrat", "(Prefers Independent Party)": "Independen", "(Prefers GOP Party)": "Republican"}
    try:
        return party_lookup[party_string]
    except KeyError:
        return "NA"
"""


def lookup_group(group_string):
    group_lookup = {"State Executive": "Executive", "Congressional": "U.S. House", "Legislative": "State Legislature"}
    return group_lookup[group_string]


races = ["Governor", "Lt. Governor", "Secretary of State", "State Treasurer", "State Auditor", "Attorney General", "Commissioner of Public Lands", "Superintendent of Public Instruction", "Insurance Commissioner"]
races += ["Congressional District 4 - U.S. Representative", "LEGISLATIVE DISTRICT 13 - State Representative Pos. 1", "LEGISLATIVE DISTRICT 13 - State Representative Pos. 2", "Legislative District 14 - State Representative Pos. 1", "Legislative District 15 - Representative, Position 1", "Legislative District 15 - Representative, Position 2",  ]

results = []

for race in races:
    race_results = {"race": race} #race variable is our shorthand name for race
    race_name = soup.find_all("RaceName", string=race) #searches for shorthand name match in official name string
    print(race_name)
    group = race_name[0].find_next_sibling("JurisdictionName") #group will be tag + contents
    print(group)
    group_cleaned = lookup_group(group.string) #match long name with shorthand
    race_results["group"] = group_cleaned
    race_results["candidates"] = []
    for hopeful in race_name:
        #counter = str(x)
        candidate = hopeful.find_next_sibling("Candidate")
        vote = hopeful.find_next_sibling("Votes")
        percent  = hopeful.find_next_sibling("PercentageOfTotalVote")
        party = hopeful.find_next_sibling("Party")
        party = party.string
        party = party.replace('Prefers', '')
        party = party.replace('(', '')
        party = party.replace(')', '')
        c_details = {"candidate": candidate.string, "vote": int(vote.string), "percent": float(percent.string),
                     "party": party}
        race_results["candidates"].append(c_details)
    print(race_results)
    results.append(race_results)

results_file = open("results.json", "w")
results_file.write(json.dumps(results, indent=4))
results_file.close()

print(json.dumps(results, indent=4))