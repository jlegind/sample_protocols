from nltk import RegexpTokenizer
import json
from ast import literal_eval
#
# t1 = 'ost er sundt'
# words = t1.split(' ')
# print(words)
# first_wordset = Levenshtein_search.populate_wordset(-1, words)
# # break
# kword = 'ost er sundt'
# kword = kword.split(' ')
# # sec_wordset = lev.populate_wordset(-1, kword)
# for j in kword:
#     rres = Levenshtein_search.lookup(first_wordset, j, 4)
#     # print('rres\n', rres[0][0], rres[0][1], rres[0][2], '\n')
#     print('rres\n', rres, '\n')

# excerpt1 = ["We","went","to","the","fire","Mother","said","Is","he","cold","Versh","Nome","Versh","said","Take","his","overcoat","and","overshoes","off","Mother","said","How","many","times","do","I","have","to","tell","you","not","to","bring","him","into","the","house","with","his","overshoes","on"]
# excerpt2 = ["Yessum","Versh","said","Hold","still","now","He","took","my","overshoes","off","and","unbuttoned","my","coat","Caddy","said","Wait","Versh","Cant","he","go","out","again","Mother","I","want","him","to","go","with","me","Youd","better","leave","him","here","Uncle","Maury","said","Hes","been","out","enough","today"]
#
# first_wordset = Levenshtein_search.populate_wordset(-1,excerpt1)
# # first_wordset = 0
# last_wordset = Levenshtein_search.populate_wordset(-1,excerpt2)
# # last_wordset = 1

import copy

d1 =  {"samplingDescription": {
    "studyExtent": "The idea is to subsample about 3% of the land area of South Northumberland and Durham ",
    "sampling": "The volunteer observers were asked to...\n1. Record all the species that they could identify confidently.\n2. Include, planted or sown plants where they are an important feature of the landscape, but to note when they are planted.\n3. To try to visit the full range of habitats within the grid square.\n4. When they had finished surveying the square, they were asked to assign a DAFOR letter to each species you found. The DAFOR scale is D = Dominant; A = Abundant, F = Frequent, O = Occasional, R = Rare.",
    "qualityControl": "Observations were digitised and reviewed by John Durkin, John O'Reily and Quentin Groom. Any obvious mistakes where deleted at this point.",
    "methodSteps": [
      "Observations were digitised using Mapmate (http://www.mapmate.co.uk/)."
    ]}
  }

def isstring(rson):
    print(rson)
    # tok = RegexpTokenizer(r'w+')
    # res = tok.tokenize(rson)
    res = remove_chars(rson)
    # print('res', res)
    ct = 0
    for w in res:
        print(w)
        ct += 1
        if ct == 10:
            break

def remove_chars(words):
    tok = RegexpTokenizer(r'\w+')
    decaf = tok.tokenize(words)
    return decaf

def isdict(rson):
    # tok = RegexpTokenizer(r'w+')
    # res = tok.tokenize(rson)
    # ct = 0
    for w in rson:
        print(w)
        # ct += 1
        # if ct == 10:
        #     break

def parson(son):
    if isinstance(son, (dict)):
        print('isDict()')
        for k in son.items():
            print(k, type(k))
            print('Field ', k[0])
            ll = len(k)
            print(ll)
            if ll > 1:
                rson = k[1]
                print(type(rson))
                parson(k[1])
            else:
                print(rson.keys())
                # res = remove_chars()

    elif isinstance(son, (str)):
        print('NOT DICT - maybe string? ', type(son))

        res = remove_chars(son)
        print(res)
    else:
        print('LIST -- maybe do something about that')
        for j in son:
            out = remove_chars(j)
            print('list item: ', out)

parson(d1)
                # print(k[1])
        # print(k, son['k'])
        #
        # for j in v.items():
        #     print(type(j))
        #     print(j[0])
        #     if isinstance(j[1], (str)):
        #         isstring(j[1])
        #     # else:

# parson(d1)

