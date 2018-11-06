from bs4 import BeautifulSoup
import requests
import re
import json

r = requests.get("https://results.vote.wa.gov/results/20181106/export/20181106_AllState.xml")
content = r.text
soup = BeautifulSoup(content, 'xml')

def lookup_party(party_string):
    party_lookup = {"(Prefers Republican Party)": "Republican", "(Prefers Democratic Party)": "Democrat", "(Prefers Independent Party)": "Independen", "(Prefers GOP Party)": "Republican"}
    try:
        return party_lookup[party_string]
    except KeyError:
        return "NA"

def lookup_group(group_string):
    group_lookup = {"State Executive": "Initatives", "Federal": "U.S. Senate", "Congressional": "U.S. House", "Legislative": "State Legislature", "Judicial": "Judicial" }
    return group_lookup[group_string]

races = ["Measure No. 1631", "Measure No. 1634", "Measure No. 1639", "Measure No. 940", "U.S. Senator", "Congressional District 4", "Congressional District 8", "District 13 - State Representative Pos. 1", "District 13 - State Representative Pos. 2", "District 14 - State Representative Pos. 1", "District 14 - State Representative Pos. 2", "District 15 - State Senator", "District 15 - State Representative Pos. 1", "District 15 - State Representative Pos. 2"]

results = [{"race":"Yakima Central Plaza Advisory Vote","group":"City of Yakima","candidate0":"Yes","party0":"NA","vote0":0,"percent0":0,"candidate1":"NO","party1":"NA","vote1":0,"percent1":0},
{"race":"Yakima County Clerk","group":"Yakima County","candidate0":"Janelle Riddel","party0":"NA","vote0":0,"percent0":0,"candidate1":"Tracey Slagle","party1":"NA","vote1":0,"percent1":0},
{"race":"Yakima County Commissioner, District 3","group":"Yakima County","candidate0":"Norm Childress","party0":"NA","vote0":0,"percent0":0,"candidate1":"Susan Soto Palmer","party1":"NA","vote1":0,"percent1":0},
{"race":"Yakima County Coroner","group":"Yakima County","candidate0":"Jack Hawkins","party0":"NA","vote0":0,"percent0":0,"candidate1":"Jim Curtice","party1":"NA","vote1":0,"percent1":0},
{"race":"Yakima County Sheriff","group":"Yakima County","candidate0":"Robert Udell","party0":"NA","vote0":0,"percent0":0,"candidate1":"Norman Wentz","party1":"NA","vote1":0,"percent1":0}]

for race in races:
    race_results = {"race": race} #race variable is our shorthand name for race
    race_name = soup.find_all("RaceName", string=re.compile(race)) #searches for shorthand name match in official name string
    #print(race_name)
    group = race_name[0].find_next_sibling("JurisdictionName") #group will be tag + contents
    #print(group)
    group_cleaned = lookup_group(group.string) #match long name with shorthand
    race_results["group"] = group_cleaned
    for x in range(0, len(race_name)):
        counter = str(x)
        candidate = race_name[x].find_next_sibling("Candidate") 
        vote = race_name[x].find_next_sibling("Votes")
        percent  = race_name[x].find_next_sibling("PercentageOfTotalVote")
        party = race_name[x].find_next_sibling("Party")
        party_cleaned = lookup_party(party.string)
        race_results["candidate" + counter] = candidate.string
        race_results["vote" + counter] = vote.string
        race_results["percent" + counter] = percent.string
        race_results["party" + counter] = party_cleaned
    #print(race_results)
    results.append(race_results)

results_file = open("results.json", "w")
results_file.write(json.dumps(results, indent=4))
results_file.close()

print(json.dumps(results))


"""for result in results:
    print(result)
    html_name = str(result['race'])
    html_name = html_name.replace(" ", "_")
    html_name = html_name + ".html"
    html_table = open(html_name, "w")
    html_table.write('<table class="table table-condensed elex-results-table"><thead><tr><th>' + str(result['race']) + '</th><th class="votes">Votes</th><th class="percent">Pct.</th><th ></th></tr></thead>')
    html_table.write('<tbody><tr><td>' + str(result['candidate0']) + '</td><td class="votes">' + str(result['vote0']) + '</td><td class="percent">' + str(result['percent0']) +'%</td><td class="pct-chart"><div class="chart-container"><div class="chart-interior" style="width:' + str(result['percent0']) + '%;"></div></div></td></tr>')
    html_table.write('<tbody><tr><td>' + str(result['candidate1']) + '</td><td class="votes">' + str(result['vote1']) + '</td><td class="percent">' + str(result['percent1']) +'%</td><td class="pct-chart"><div class="chart-container"><div class="chart-interior" style="width:' + str(result['percent1']) + '%;"></div></div></td></tr></tbody></table>')
    html_table.close()

m1631 = soup.find_all("RaceName", string=re.compile("Measure No. 1631"))
for result in m1631:
    counter = 1
    candidate = result.find_next_sibling("Candidate")
    vote = result.find_next_sibling("Votes")
    percent = result.find_next_sibling("PercentageOfTotalVote")


#x = races.find_all("RaceName", string=re.compile("Measure No. 1631"))
print(m1631)"""