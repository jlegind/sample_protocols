import nltk
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
import pandas as pd


search_url = 'http://api.gbif.org/v1/dataset/search?q='
terms = ['LTER', 'DAFOR', 'transect', 'quadrat', 'census', 'drones', 'field work']
cols = ['field', 'term', 'datasetkey', 'accurates', 'close-enough', 'distance', 'number']
dframe = pd.DataFrame(columns=cols)
fields = ['title', 'description', 'samplingDescription']
dct = {}
dct['number'] = 0
d1 =  {"samplingDescription": {
    "studyExtent": "The idea is to subsample about 3% of the land area of South Northumberland and Durham ",
    "sampling": "The volunteer observers were asked to...\n1. Record all the species that they could identify confidently.\n2. Include, planted or sown plants where they are an important feature of the landscape, but to note when they are planted.\n3. To try to visit the full range of habitats within the grid square.\n4. When they had finished surveying the square, they were asked to assign a DAFOR letter to each species you found. The DAFOR scale is D = Dominant; A = Abundant, F = Frequent, O = Occasional, R = Rare.",
    "qualityControl": "Observations were digitised and reviewed by John Durkin, John O'Reily and Quentin Groom. Any obvious mistakes where deleted at this point.",
    "methodSteps": [
      "Observations were digitised using Mapmate (http://www.mapmate.co.uk/)."
    ]}
  }

def isstring(rson, term, field, dct, datasetkey):
    print(rson)
    res = remove_chars(rson)
    for word in res:
        sendback = test_distance(word, term, field, dct, datasetkey)
    return sendback

def remove_chars(words):
    tok = nltk.RegexpTokenizer(r'\w+')
    decaf = tok.tokenize(words)
    return decaf

def test_distance(word, kword, field, dct, datasetkey):
    print('///RUNNING TEST_DISTANCE()')
    if 'number' not in dct.keys():
        dct['number'] = 0
    dct['field'] = field
    word = word
    if isinstance(word, (list))== False:
        word = word.lower()

    print(word, "######test_distance##")
    print('currentt dict: ', dct)
    dist = nltk.edit_distance(kword, word)
    print(word, dist)
    if dist == 1:
        dct['close-enough'] = word
        dct['distance'] = dist
        dct['number'] += 1
        print("--success--\n ", word)
    if dist == 0:
        dct['datasetkey'] = datasetkey
        dct['accurates'] = word
        dct['distance'] = dist
        if dct['datasetkey'] == datasetkey and dct['term'] == kword and dct['field'] == field:
            dct['number'] += 1
        print("--success--\n ", word)
    if dct['number'] > 0:
        return dct

def parson(son, term, field, dct, datasetkey):
    dct['term'] = term
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
                parson(k[1], term, field, dct, datasetkey)
            else:
                print(rson.keys())
                # res = remove_chars()

    elif isinstance(son, (str)):
        print('NOT DICT - maybe string? ', type(son))
        res = isstring(son, term, field, dct, datasetkey)

        print(res)
        return res
    else:
        print('LIST -- maybe do something about that')
        for j in son:
            out = remove_chars(j)
            print('list item: ', out)


news = parson(d1, 'dafor', "samplingDescription", dct, '5d784d06-fa1d-4f00-8cdc-663d04d26061')
print(news)
