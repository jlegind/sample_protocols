import nltk
import requests
import copy
import pandas as pd
import responses


search_url = 'http://api.gbif.org/v1/dataset/search?q='
# terms = ['LTER', 'DAFOR', 'transect', 'quadrat', 'census', 'drones', 'field work']
terms = ('quadrat',)
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
    # surl = api+'{}'.format(term)
    print(api)
    response = requests.get(api)
    rson = response.json()
    # results = rson['results']
    return(rson)

def dataset_metadata_lookup(datasetkey, field, api='http://api.gbif.org/v1/dataset/'):
    print('RUNNING DATASET METADATA LOOKUP********')
    url = api+'{}'.format(datasetkey)
    res = gbif_api(url, datasetkey)
    try:
        res = res[field]
        return res
    except KeyError as e:
        print('After metadata lookup -- KEYERROR')

def isstring(rson, term, field, datasetkey):
    print('iss dct', dct)
    print('isstrterm: ', term)
    res = remove_chars(rson)
    for word in res:
        sendback = test_distance(word, term, field, datasetkey)
    return sendback

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

def test_distance(word, kword, field, datasetkey):
    print('///RUNNING TEST_DISTANCE() on field ', field)
    #print('len dct: {}'.format(len(dct), dct))
    # for j in dct:
    #     # print(dct)
    #     inside = dct[j]
    #     print('inside type ', type(inside), inside)
    #     for k, v in inside.items():
    #         # print(k)
    #         if k == 'term': inside[k] = kword
    #         if k == 'field': inside[k] = field
    #         if k == 'datasetkey': inside[k] = datasetkey
    # print('after forkv: ', dct)
    # accdct = dct['accurate']
    # close_dict = dct['close_dict']
    # if 'number' not in dct.keys():
    #     print('not in dctkeys')
    #     #dct['number'] = 0
    # dct['field'] = field
    # cdct = {}
    # cdct['term'] = kword
    # cdct['field'] = field
    # cdct['number'] = 0

    if isinstance(word, (list))== False:
        word = word.lower()

    print(word, kword, "######test_distance##")
    # print('currentt dict: ', dct)
    dist = nltk.edit_distance(kword, word)
    print(word, dist)
    if dist == 1:
        # cdct = close_dict
        # cdct['datasetkey'] = datasetkey
        # cdct['close-enough'] = word
        # cdct['distance'] = dist
        # if cdct['datasetkey'] == datasetkey and cdct['term'] == kword and cdct['field'] == field:
        #     cdct['number'] += 1
        print("--success--\n ", word)
        # print('copy dict: ', cdct)
        close_pair = (kword, word, dist, field, datasetkey)
        return close_pair
    if dist == 0:
        # accdct['datasetkey'] = datasetkey
        # accdct['accurates'] = word
        # accdct['distance'] = dist
        # if accdct['datasetkey'] == datasetkey and accdct['term'] == kword and accdct['field'] == field:
        #     accdct['number'] += 1
        print("--success--\n ", word)
        acc_pair = (kword, word, dist, field, datasetkey)
        return acc_pair
    # print('before return', dct)
    # if dct['number'] > 0:
    #     print('biggger than zero')

    #return dct

def parson(son, term, field, dct, datasetkey):
    print('###PARSON STARTED with term: ', term, datasetkey)
    # dct['term'] = term
    # dct['field'] = field
    orgfield = copy.copy(field)
    print('orgfield ', orgfield)
    if isinstance(son, (dict)):
        print('isDict()')
        for k in son.items():
            # print(k, 'and type: ', type(k))
            print('Field ', k[0])
            if k[0] != field:
                #
                # print('NOT term')
                continue
            else:
                print('TERM iss')
            field = k[0]
            if orgfield != field:
                print('orgfield is superceded by new field')
                dct['number'] = 0
            ll = len(k)
            print('kfield', ll)
            if ll > 1:
                rson = k[1]
                print(rson)
                print('!type: ', type(rson))
                if isinstance(rson, (list)):
                    islist(rson)
                else:
                    print('Yield in parson()')
                    # yield from parson(rson, term, field, dct, datasetkey)
            else:
                print(rson.keys())

    elif isinstance(son, (str)):
        print('NOT DICT - maybe string? ', type(son))
        print('string term and key', term, datasetkey)
        res = isstring(son, term, field, datasetkey)
        print('parson res tuple: ', res)
        if not res:
            print('none', res)
        else:
            print('inside else : ', res)
            yield res
    else:
        print('LIST -- maybe do something about that')

search_url = 'http://api.gbif.org/v1/dataset/search?q='
dlist = []
#A break pad !!!
limiter = 12

thedct = {"accurate":{'term': '', 'field': '', 'number': 0, 'datasetkey': '', 'accurates': '', 'distance': None},
          "close_dict":{'term': '', 'field': '', 'number': 0, 'datasetkey': '', 'accurates': '', 'distance': None}}

for t in terms:
    res = term_api_search(search_url, t)
    ct = 0
    for j in res['results']:
        ct += 1
        if ct > limiter: break
        # print(j)
        print('jkey', j['key'])
        datasetkey = j['key']
        print('jkey is : ', datasetkey)
        print('acute term list: {} - key {}'.format(terms, datasetkey))
        for f in fields:
            lookup = dataset_metadata_lookup(datasetkey, f)
            print(lookup)
            # newdct = {}
            print('news and key: ', datasetkey)
            news = parson(lookup, t, f, thedct, datasetkey)
            print('str yield generator')
            print('tis: ', t)
            for n in news:
                print('inside generator')
                print('gg ', n)
                term = n[0]
                word = n[1]
                distance = n[2]
                field = n[3]
                print('{} has {} in field: {} that matches {} at distance {}'.format(datasetkey, term, field, word, distance))
                # (kword, word, dist, field, datasetkey)
                #for d, elem in n.items():
                # for key in n:
                #
                #     if n['number'] != 0:
                #         print('notzero')
                #         nary = copy.copy(n)
                #         print('nary ', nary)
                #         dlist.append(nary)
                # #         print('not zero')
                #         dlist.append(copy.copy(j))
                # for n in j:
                #     print('news', type(n), n)
                #     if n['number'] != 0:
                #         print('not zero')
                #         dlist.append(copy.copy(j))
                print(dlist)
                ct += 1

print('longlist: ', dlist)
for item in dlist:
    print('final list: ', item)

