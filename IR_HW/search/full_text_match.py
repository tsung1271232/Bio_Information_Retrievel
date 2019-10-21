import re

data_path = "/home/tsung/CODE/Information-Retrieval/IR_HW/search/data/match_data"

color_table = ["#FFFF00", "#00FFFF"]

class xmldata:
    def __init__(self, title=None, content=None, char_count=None, word_count=None, sentence_count=None, score=None):
        self.title = title
        self.content = content
        self.char_count = char_count
        self.word_count = word_count
        self.sentence_count = sentence_count
        self.score = score


def match_and_insert(match, key, str, score, weight):
    new_str = ""
    new_content = ""
    match_idx = []

    for idx in list(re.finditer(key, str.lower())):
        match_idx.append((idx.start(), idx.end()))
        score = score + weight
        match = True
    # add font color tag
    if(len(match_idx) > 0):
        j = 0
        # iterate each char
        for i in range(len(str)):
            if(i == match_idx[j][0]):
                new_str = new_str + \
                    '<span style="background-color:#FFFF00">' + str[i]
            elif(i == match_idx[j][1]):
                new_str = new_str + '</span>' + str[i]
                j = j + 1
                if(j >= len(match_idx)):
                    new_str = new_str + str[i + 1:]
                    break
            else:
                new_str = new_str + str[i]
        str = new_str

    return match, str, score


def full_text_match(file_name, key):
    key = key.lower()
    match = False
    match_data = []

    key = key.split(' ')

    with open(file_name, "r", encoding='UTF-8') as inputFile:
        line = inputFile.readline()
        i = 0
        while line:
            match = False
            data = line.split('\t')
            # print("i = ",i, "len" , len(data), data[2])
            i = i+1
            title = data[0]
            content = data[1]
            char_count = data[2]
            word_count = data[3]
            sentence_count = data[4].strip()

            if(sentence_count[-1] == '\n'):
                print("error")

            score = 0
            # weight for multiple match
            pre_score = 0
            weight = 0
            # match title
            for each in key:
                match, title, score = match_and_insert(
                    match, each, title, score, 100)
                match, content, score = match_and_insert(
                    match, each, content, score, 10)
                if(score != pre_score):
                    weight = weight + 1
                pre_score = score

            score = score * (10 ** weight)
            
            # save matching data
            if(match == True):
                match_data.append(
                    xmldata(title, content, char_count, word_count, sentence_count, score))
            line = inputFile.readline()

        match_data.sort(key=lambda x: x.score, reverse=True)

    with open(data_path, 'w', encoding='UTF-8') as outputFile:
        for i in match_data:
            output = '%s\t%s\t%s\t%s\t%s\t%d\n' % (
                i.title, i.content, i.char_count, i.word_count, i.sentence_count, i.score)
            outputFile.write(output)

    return match_data
