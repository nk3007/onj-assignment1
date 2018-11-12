import csv
import re
from collections import Counter


class ClResults:

    def __init__(self, fileName):
        self.ids = []
        self.matchInfo = {}
        self.titles = {}

        with open(fileName, 'rt', encoding="utf8") as file:
            reader = csv.reader(file, delimiter=',')
            # get header
            headers = file.readline().split(",")
            title_i, match_info_i = headers.index("title"), headers.index("match_info\n")
            for line in reader:
                # skip null values
                if not line[title_i] == "null":
                    self.ids.append(line[0])
                    self.titles[line[0]] = line[title_i]
                    # remove newLines, because of data
                    self.matchInfo[line[0]] = " ".join(str(line[match_info_i]).replace("\n", "").split())

    def getResults(self):
        results = {}
        for key, info in self.matchInfo.items():
            regex_stadium = "([\w\s.]+) (\d+ : \d+) ([^\d\W\s.]+)"
            stadium_pattern = re.compile(regex_stadium)
            match = stadium_pattern.search(info)
            results[match.group(1) + "-" + match.group(3)] = match.group(2)

        return results

    def getReferee(self):
        referees = []
        for key, info in self.matchInfo.items():
            regex_referee = "Sodnik: ([\w\s]+)"
            referee_pattern = re.compile(regex_referee)
            match = referee_pattern.search(info)
            referees.append(match.group(1))
        return Counter(referees)

    def getScorers(self):
        scorers = []
        for key, info in self.matchInfo.items():
            regex_scorer_home = "'([\w\s]+)[\(11m\)]*(\d+ : \d?) "
            referee_scorer_home = re.compile(regex_scorer_home)
            match_home = referee_scorer_home.findall(info)

            regex_scorer_away = "(\d+ : \d+)\'([\w\s]+[^\d\W])"
            referee_scorer_away = re.compile(regex_scorer_away)
            match_away = referee_scorer_away.findall(info)

            scorers.append(i[0] for i in match_home)
            scorers.append(i[1] for i in match_away)

        # flatten
        scorers = [item for sublist in scorers for item in sublist]
        return Counter(scorers)


data = ClResults("./data/nogomania-cl-results.csv")

print(data.getResults())
print("Top 5 most common referees: ", data.getReferee().most_common(5))
print("Top 3 goal scorer: ", data.getScorers().most_common(3))
