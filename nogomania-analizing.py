import csv
from collections import Counter
from nltk import word_tokenize, pos_tag, ne_chunk, Text


class FootballAnalyzing:

    def __init__(self, fileName):
        self.ids = []
        self.titles = {}
        self.comments_num = {}
        self.subjects = {}
        self.descriptions = {}
        with open(fileName, 'rt', encoding="utf8") as file:
            reader = csv.reader(file, delimiter=',')
            # get header
            headers = file.readline().split(",")
            title_i, subject_i, comment_num_i, description_i = headers.index("title"), headers.index(
                "subject"), headers.index("comment_number"), headers.index("description")
            for line in reader:
                # skip null values
                if not line[title_i] == "null":
                    self.ids.append(line[0])
                    self.titles[line[0]] = line[title_i]
                    self.comments_num[line[0]] = line[comment_num_i]
                    self.subjects[line[0]] = line[subject_i]
                    self.descriptions[line[0]] = line[description_i]

    def getSubjectPecentage(self):
        counter = Counter(self.subjects.values())
        return [(i, counter[i] / len(self.subjects) * 100.0) for i in counter]

    def getTokens(self):
        tokens = word_tokenize(self.descriptions[self.ids[0]])
        print("Tokens: ", tokens)

        # Syntax Level
        tagged_tokens = pos_tag(tokens)
        print("POS tagging:", tagged_tokens)

        # Semantics Level
        ner_tree = ne_chunk(tagged_tokens)
        # print("Light parsing:", ner_tree)

        all_desc_tokens = word_tokenize(''.join(str(x) for x in self.descriptions.values()).lower())
        text = Text(all_desc_tokens)
        text.similar("napadalec", 5)


data = FootballAnalyzing("../data/nogomania-descriptions.csv")
# print(data.titles)
# print(len(data.titles))
print(data.getSubjectPecentage())
data.getTokens()
