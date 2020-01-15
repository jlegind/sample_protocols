import requests
import nltk
import re
import nltk
import requests
import pandas as pd
import os
from collections import ChainMap
import csv

# from bs4 import BeautifulSoup as bs


search_url = 'http://api.gbif.org/v1/dataset/search?q='
secndAPI = 'http://api.gbif.org/v1/dataset/'
# terms = ['LTER', 'DAFOR', 'transect', 'quadrat', 'census', 'Braun-Blanquet']
terms = ['reineck']
cols = ['field', 'term', 'datasetkey', 'accurates', 'close-enough', 'distance', 'number']
# dframe = pd.DataFrame(columns=cols)
fields = ['title', 'description', 'samplingDescription']
lofdicts = []

f = open('dictcsv.csv', 'w')


def gbif_api(api, term):
    surl = api+'{}'.format(term)
    print(surl)
    response = requests.get(surl)
    rson = response.json()
    # results = rson['results']
    return(rson)


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
        return dct
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
    print('WHICH FIELD ??? - ', field, datasetkey)
    kword = term.lower()
    dct = {'field': field}
    dct['number'] = 0
    dct['accurates'] = 0
    dct['distance'] = 0
    dct['close-enough'] = 0
    dct['datasetkey'] = datasetkey
    dct['term'] = term
    search = api+'{}'.format(datasetkey)
    print(search)
    response = requests.get(search)
    rson = response.json()
    print('rson', rson)
    datasetkey = rson['key']

    try:
        results = rson[field]
        print('init res::: ', results)
        with open('dictcsv.csv', 'a') as g:

        # dlist = []
            if isinstance(results, (dict)):
                print('WWe have a dict }}}')
                print(list(results.values())[0], "RES VAL")
                unpacked = list(results.values())[0]
                print(type(unpacked[0]))
                if unpacked[0]:
                    for key, val in results.items():
                        print('wwwe have key == ', key, 'And have value ==type ', type(val), val)
                        newdct = {'datasetkey': datasetkey}
                        newdct['field'] = key
                        newdct['number'] = 0
                        field = key
                        print('"""field"""=', key)
                        newdct['term'] = kword
                        newdct['accurates'] = 0
                        newdct['distance'] = None
                        newdct['close-enough'] = None
                        print('##field ', field)
                        # with open('dictcsv.csv', 'a') as g:
                        if isinstance(val, (list)):
                            print('¤¤¤WE HAVE A LIST¤¤¤')
                            if len(val) == 0:
                                print('val length is = ', len(val))
                                break
                            for text in val:
                                twords = text.split()
                                for word in twords:
                                    g = test_distance(word, kword, field, newdct, datasetkey)
                                if g:
                                    lofdicts.append(g)
                                    print('write list', g)

                                    writer = csv.writer(g)
                                    for key in g.keys():
                                        writer.writerow(key, g[key])

                                print('ddd', lofdicts)

                        else:
                            val = val.split()
                            for word in val:
                                g = test_distance(word, kword, field, newdct, datasetkey)
                                writer = csv.writer(g)
                                print('write dict', g)
                                for key in g.keys():
                                    writer.writerow(key, g[key])
                                if g:
                                    lofdicts.append(g)
                            print('ddd', lofdicts)
                    return lofdicts
                else:
                    print('{} is [None]'.format(results))
            # elif isinstance(results, (list)):
            #     print('A LIST!!')
            else:
                print('its A string!!')
                newdct = {'datasetkey': datasetkey}
                newdct['field'] = rson
                newdct['number'] = 0
                # field =
                # print('"""field"""=', key)
                newdct['term'] = kword
                newdct['accurates'] = 0
                newdct['distance'] = None
                newdct['close-enough'] = None
                lres = results.split()
                for j in lres:
                    dct['field'] = f
                    print('"""field"""=', f)
                    dct['term'] = kword
                    print('##test dist {}'.format(j))
                    g = test_distance(j, kword, field, dct, datasetkey)
                    if g:
                        print('we have G')
                        lofdicts.append(g)
                        writer = csv.writer(g)
                        print('write string', g)
                        for key in g.keys():
                            writer.writerow(key, g[key])
                    print('ddd', lofdicts)
                return lofdicts
    except (KeyError, TypeError) as e:
        # raise Exception('No matching key!!!')
        print(type(e), e)
        print('THE DATASET WITH KEY = {} HAS ..NO.. FIELD NAMED = "{}"'.format(datasetkey, field))
        pass


def dataset_api_search(api, term, field):
    print('###dataset_api_search##')
    field = field
    kword = term.lower()
    dct = dict()
    search = api+'{}{}'.format(term, '&limit=200')
    # search = api + '{}{}{}'.format(term, '&publishingOrg=e6e855d7-9775-400f-883b-c4e04e517d79','&limit=200')
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
            print('{} ffield {} = \n{}'.format(datasetkey, field, lookup))
        except (KeyError, TypeError) as e:
            print(type(e), e)
    if not lookup:
        print('Lookup is "NoneType"')
    else:
        print('==: this is return lookup len{}: '.format(len(lookup), lookup))
    if lookup:
        if isinstance(lookup, (list)):
            print('LIST OOPS: {}'.format(lookup))
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
# distilled = pd.DataFrame()
for f in fields:
    for t in terms:
        res = dataset_api_search(search_url, t, f)


        print('BEGIN LOOP ==== {} ** {}'.format(type(res), res))
        # res = filter(None, res)
        if res:
            try:
                distilled = pd.DataFrame(res)
                # distilled = distilled.set_index(res, ignore_index=True)
                # distilled = distilled.append(res, ignore_index=True)
                # distilled = pd.DataFrame.from_records(res, index= ['datasetkey'])
                print('%%', distilled.to_string(), '%%')
                distilled = distilled.reindex(columns=cols)
                # res = dataset_meta_lookup(secndAPI, 'd0582993-28ac-4ac4-937d-cb61497e532c', 'quadrat', f)
                lofdicts.append(res)

                print('final res =', lofdicts)
                print('final distilled =\n', distilled.to_string())

                distilled = distilled.append(res, ignore_index=True)
            except AttributeError:
                pass

            distilled = distilled.dropna(subset=['distance', 'datasetkey'])
            print(distilled.to_string())

        else:
            print('EMPTY RES - LIST LEN = 0')


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