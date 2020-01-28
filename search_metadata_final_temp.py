import requests
import nltk
import re
import nltk
import requests
import pandas as pd
import os

# from bs4 import BeautifulSoup as bs


search_url = 'http://api.gbif.org/v1/dataset/search?q='
secndAPI = 'http://api.gbif.org/v1/dataset/'
# terms = ['LTER', 'DAFOR', 'transect', 'quadrat', 'census', 'field work']
terms = ['quadrat']
cols = ['field', 'term', 'datasetkey', 'accurates', 'close-enough', 'distance', 'num'
                                                                                'ber']
dframe = pd.DataFrame(columns=cols)
fields = ['title', 'description', 'samplingDescription']
lofdicts = []



def gbif_api(api, term):
    surl = api+'{}'.format(term)
    print(surl)
    response = requests.get(surl)
    rson = response.json()
    # results = rson['results']
    return(rson)



def terms_lookup(term, api, dataframe, field):
    if (field not in fields):
        raise Exception('Field not a member !!!! Allowed values are: {}'.format(fields))
    kword = term.lower()
    dframe = dataframe
    a_field = field
    surl = api+'{}{}'.format(term, "&type=OCCURRENCE&limit=200")
    print(surl)

    response = requests.get(surl)
    rson = response.json()
    results = rson['results']

    # ind = 0

    for j in results:
        try:
            # print(j['description'])
            print("#####try  ", a_field)

            title = j[a_field]
        except KeyError:
            continue
        # dct = dict()
        dct['field'] = field
        dct['term'] = kword


        print('## ',j['key'])
        words = title.split(' ')
        # print(words)
        # kword = term
        # print(kword, '\n######')
        for word in words:
            word = word.lower()
            dist = nltk.edit_distance(kword, word)
            print('¤¤word - distance == ', word, dist)
            if dist == 1:
                # lter_title['close'].append([j['key'], word])
                dct['close-enough'] = [word, dist]
                dct['number'] += 1

            if word == kword and dist == 0:
                # lter_title['lter'].append(j['key'])
                dct['datasetkey'] = j['key']
                dct['accurates'] = word
                dct['number'] += 1
                print('==success dict : ', dct)
                print("--success--\n ", word)
        print('THE DICT:: ', dct)
        dframe = dframe.append(dct, ignore_index=True)
    dframe = dframe[pd.notnull(dframe['datasetkey'])]
    return(dframe)

# fields = ['samplingDescription']


def test_distance(word, kword, field, dct, datasetkey):
    print('///RUNNING TEST_DISTANCE()')
    # dct['field'] = field

    word = word
    if isinstance(word, (list))== False:
        word = word.lower()

    print('currentt dict: ', dct)
    dist = nltk.edit_distance(kword, word)
    print(word, dist)
    if dist == 1:
        dct['close-enough'] = word
        dct['distance'] = dist
        dct['number'] += 1
        print("--1success--\n ", word)
    if dist == 0:
        dct['datasetkey'] = datasetkey
        dct['accurates'] = word
        dct['distance'] = dist
        print('san chck - ', dct)
        print('precondition', dct['datasetkey'],dct['term'], dct['field'])
        if dct['datasetkey'] == datasetkey and dct['term'] == kword and dct['field'] == field:
            dct['number'] += 1
        print("--0success--\n ", word)
    return dct


def dataset_meta_lookup(api: object, datasetkey: object, term: object, field: object) -> object:
    print('###dataset_metadata_lookup##')
    field = field
    print('WHICH FIELD ??? - ', field )
    kword = term.lower()
    dct = {'field': field}
    dct['number'] = 0
    dct['datasetkey'] = datasetkey
    dct['term'] = term
    search = api+'{}'.format(datasetkey)
    print(search)
    response = requests.get(search)
    rson = response.json()
    datasetkey = rson['key']
    try:
        results = rson[field]
        print('init res::: ', results)

        dlist = []
        if isinstance(results, (dict)):
            print('WWe have a dict }}}')
            for key, val in results.items():
                print('wwwe have key == ', key, 'And have value ==type ', type(val), val)
                newdct = {'datasetkey': datasetkey}
                newdct['field'] = key
                newdct['number'] = 0
                field = key
                print('"""field"""=', key)
                newdct['term'] = kword
                print('##field ', field)
                if isinstance(val, (list)):
                    print('¤¤¤WE HAVE A LIST¤¤¤')
                    if len(val) == 0:
                        print('val length is = ', len(val))
                        break
                    for text in val:
                        twords = text.split()
                        for word in twords:
                            g = test_distance(word, kword, field, newdct, datasetkey)
                        dlist.append(g)
                else:
                    val = val.split()
                    for word in val:
                        g = test_distance(word, kword, field, newdct, datasetkey)
                    dlist.append(g)
            return dlist
        # elif isinstance(results, (list)):
        #     print('A LIST!!')
        else:
            print('its A string!!')
            lres = results.split()
            for j in lres:
                dct['field'] = f
                print('"""field"""=', f)
                dct['term'] = kword
                print('##test dist {}'.format(j))
                g = test_distance(j, kword, field, dct, datasetkey)
            return g
    except KeyError:
        # raise Exception('No matching key!!!')
        print('THE DATASET WITH KEY = {} HAS ..NO.. FIELD NAMED = "{}"'.format(datasetkey, field))
        pass


def dataset_api_search(api, term, field):
    print('###dataset_api_search##')
    field = field
    kword = term.lower()
    dct = dict()
    search = api+'{}{}'.format(term, '&limit=200')
    print(search)
    response = requests.get(search)
    rson = response.json()
    results = rson['results']
    print('RR -- ', results)
    lookup = ''
    # g = dict()
    # returnlist = []
    for j in results:
        print('TYPE', type(j))
        print(j['key'])
        try:
            print('####FIELD TITLE###', field, type(j))
            datasetkey = j['key']
            lookup = dataset_meta_lookup(secndAPI, datasetkey, kword, field)
            print('tyype lookupp', type(lookup))
            print(len(lookup), "%%")
        except KeyError:
            print('No matching key!!!', datasetkey)
    return lookup
        # dct=dict()
        # dct['field'] = field
        # dct['term'] = kword
        # datasetkey = j['key']
        # print("now dict --- ", dct)
        #     # try:
        # print('after dataset_metadata_lookup loop/// ')
        # try:
        #     res =  lookup[field]



# res = terms_lookup('LTER', search_url, dframe, 'description')
distilled = dframe
for f in fields:
    for t in terms:
        res = dataset_api_search(search_url, t, f)
        print('BEGIN LOOP ==== ', res)
        # res = filter(None, res)
        # distilled = distilled.append(res, ignore_index=True)
        # distilled = pd.DataFrame.from_records(res, index= ['datasetkey'])
        # distilled = distilled[cols]
# , index=['datasetkey'])
    # res = dataset_meta_lookup(secndAPI, '5d784d06-fa1d-4f00-8cdc-663d04d26061', 'dafor', f)
        lofdicts.append(res)
    print('final res =', lofdicts)
    distilled = distilled.append(res, ignore_index=True)

distilled = distilled.dropna(subset=['distance', 'datasetkey'])
print(distilled.to_string())

# dflist = list()
#
# for j in fields:
#     print("starting field = {}".format(j))
#     for k in terms:
#         print("starting term = {}".format(k))
#         res = terms_lookup(k, search_url, dframe, j)
#
#         if not res.empty:
#             dflist.append(res)
#             print('RESSS', dflist)
#
#         print('----------------------------')
#     fin = pd.concat(dflist)
# print(fin.to_string())
#
# directory = 'C:/Users/jlegind/PycharmProjects/sample_protocols/'
# file = 'sampleevent.csv'
# fin.to_csv(os.path.join(directory, file))