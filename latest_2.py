import nltk
import requests
import copy
import pandas as pd
import responses


search_url = 'http://api.gbif.org/v1/dataset/search?q='
# terms = ['LTER', 'DAFOR', 'transect', 'quadrat', 'census', 'drones', 'field work']
terms = ['quadrat']
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
def gbif_api(api, term):
    surl = api+'{}'.format(term)
    print(surl)
    response = requests.get(surl)
    rson = response.json()
    # results = rson['results']
    return(rson)

def isstring(rson, term, field, dct, datasetkey):
    print(rson)
    res = remove_chars(rson)
    for word in res:
        sendback = test_distance(word, term, field, dct, datasetkey)
    return sendback

def islist(rson):
    print('Some list to think about')
    print(rson)

def remove_chars(words):
    tok = nltk.RegexpTokenizer(r'\w+')
    decaf = tok.tokenize(words)
    return decaf

def term_api_search(api, term):
    print('###dataset_api_search##')
    # kword = term.lower()
    # dct = dict()
    search = api+'{}{}'.format(term, '&limit=200')
    print(search)
    response = requests.get(search)
    rson = response.json()
    return rson

def test_distance(word, kword, field, dct, datasetkey):
    print('///RUNNING TEST_DISTANCE() on field ', field)
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
        print('biggger than zero')
        return dct

def dataset_metadata_lookup(datasetkey, field, api='http://api.gbif.org/v1/dataset/'):
    print('RUNNING DATASET METADATA LOOKUP********')
    url = api+'{}'.format(datasetkey)
    res = gbif_api(api, datasetkey)
    return res

def parson(son, term, field, dct, datasetkey):
    print('###PARSON STARTED')
    dct['term'] = term
    dct['field'] = field
    orgfield = copy.copy(dct['field'])
    print('orgfield ', orgfield)
    if isinstance(son, (dict)):
        print('isDict()')
        for k in son.items():
            print(k, 'and type: ', type(k))
            print('Field ', k[0])
            if k[0] != field:
                print('NOT term')
                continue
            else:
                print('TERM iss')
            field = k[0]
            if orgfield != field:
                print('orgfield is superceded by new field')
                dct['number'] = 0
            ll = len(k)
            print(ll)
            if ll > 1:
                rson = k[1]
                print(rson)
                print('!type: ', type(rson))
                if isinstance(rson, (list)):
                    islist(rson)
                else:
                    yield from parson(rson, term, field, dct, datasetkey)
            else:
                print(rson.keys())

    elif isinstance(son, (str)):
        print('NOT DICT - maybe string? ', type(son))
        res = isstring(son, term, field, dct, datasetkey)
        if not res:
            print('none', res)
        else:
            print('inside else : ', res)
            yield res
    else:
        print('LIST -- maybe do something about that')

search_url = 'http://api.gbif.org/v1/dataset/search?q='
dlist = []

for t in terms:
    res = term_api_search(search_url, t)
    for j in res['results']:
        # print(j)
        print(j['key'])
        
    break
    news = parson(d2, t, f, dct, 'a855a185-cf36-4b06-89f6-bbbce2e2805d')
    print('str yield generator')
    for j in news:
    # while
        print('inside generator')
        print('gg ', j)
        if j['number'] != 0:
            print('not zero')
            dlist.append(copy.copy(j))
        print(dlist)

print('final list: ', dlist)

# def dataset_api_search(api, term, field):
#     print('###dataset_api_search##')
#     field = field
#     kword = term.lower()
#     # dct = dict()
#     search = api+'{}{}'.format(term, '&limit=200')
#     print(search)
#     response = requests.get(search)
#     rson = response.json()
#     results = rson['results']
#     print('RR -- ', results)
#     lookup = ''
#     # g = dict()
#     # returnlist = []
#     for j in results:
#         print('TYPE', type(j))
#         print(j['key'])
#         try:
#             print('####FIELD TITLE###', field, type(j))
#             datasetkey = j['key']
#             lookup = dataset_metadata_lookup(datasetkey, field)
#             # print('tryy lookupp', lookup)
#             print(lookup[field], "%%")
#         except KeyError:
#             print('No matching key!!!', datasetkey)
#         # dct=dict()
#         dct['field'] = field
#         dct['term'] = kword
#         datasetkey = j['key']
#         print("now dict --- ", dct)
#             # try:
#         print('after dataset_metadata_lookup loop/// ')
#         try:
#             res =  lookup[field]
#         except KeyError:
#             print('After lookup KEYERROR')
#             continue
#         print('RESS:  ', res)
#         print('IS DICT??:  ', type(res))
#
#         if isinstance(res, (dict)):
#             print("IS A DICT() ")
#             # for v in res:
#             #     tok = nltk.RegexpTokenizer(r'\w+')
#             #     if isinstance(v, (list)):
#             #         v = ''.join(j for j in v)
#             #     out = tok.tokenize(v)
#             #     print('THISIS OUT:::', out)
#             for k, val in res.items():
#
#
