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

def dataset_metadata_lookup(datasetkey, field, api='http://api.gbif.org/v1/dataset/'):
    print('RUNNING DATASET METADATA LOOKUP********')
    url = api+'{}'.format(datasetkey)
    res = gbif_api(api, datasetkey)
    try:
        res = res[field]
        return res
    except KeyError as e:
        print('After metadata lookup -- KEYERROR')

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
        dct['datasetkey'] = datasetkey
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

def parson(son, term, field, dct, datasetkey):
    print('###PARSON STARTED')
    dct['term'] = term
    dct['field'] = field
    orgfield = copy.copy(dct['field'])
    print('orgfield ', orgfield)
    if isinstance(son, (dict)):
        print('isDict()')
        for k in son.items():
            # print(k, 'and type: ', type(k))
            print('Field ', k[0])
            if k[0] != field:
                # print('NOT term')
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
    ct = 0
    for j in res['results']:
        ct += 1
        if ct > 10: break
        # print(j)
        print(j['key'])
        datasetkey = j['key']
        for f in fields:
            lookup = dataset_metadata_lookup(datasetkey, f)
            print(lookup)
            newdct = {}
            news = parson(lookup, t, f, newdct, datasetkey)
            print('str yield generator')
            # ct = 0
            for j in news:
            # while
                print('inside generator')
                print('gg ', j)
                if j['number'] != 0:
                    print('not zero')
                    dlist.append(copy.copy(j))
                print(dlist)
                ct += 1


for item in dlist:
    print('final list: ', item)

