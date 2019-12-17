import nltk
import requests
import pandas as pd
import copy
import os

# from bs4 import BeautifulSoup as bs


search_url = 'http://api.gbif.org/v1/dataset/search?q='
terms = ['LTER']
# , 'DAFOR']
    # , 'transect', 'quadrat', 'census', 'drones', 'field work']
cols = ['field', 'term', 'datasetkey', 'accurates', 'close-enough', 'distance', 'meta_content']
dframe = pd.DataFrame(columns=cols)
fields = ['title', 'description', 'samplingDescription']
retlist = []
#


def gbif_api(api, term):
    surl = api+'{}'.format(term)
    print(surl)
    response = requests.get(surl)
    rson = response.json()
    # results = rson['results']
    return(rson)

secndAPI = 'http://api.gbif.org/v1/dataset/'
# fields = ['samplingDescription']



def dataset_metadata_lookup(datasetkey, field, api='http://api.gbif.org/v1/dataset/'):
    print('RUNNING DATASET METADATA LOOKUP********')
    url = api+'{}'.format(datasetkey)
    res = gbif_api(api, datasetkey)
    return res

def test_distance(word, kword, dct, datasetkey):
    print('RUNNING TEST_DISTANCE()', datasetkey)
    dct = dct
    word = word
    if isinstance(word, (list))== False:
        word = word.lower()

    print(word, "######test_distance##")
    dist = nltk.edit_distance(kword, word)
    print(word, dist)
    if dist == 1:
        dct['close-enough'] = word
        dct['distance'] = dist
        print(dct)
        return dct
    if dist == 0:
        dct['datasetkey'] = datasetkey
        dct['accurates'] = word
        dct['distance'] = dist
        print('SUCCCESSSS')
        print(dct)
        return dct



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
            lookup = dataset_metadata_lookup(datasetkey, field)
            # print('tryy lookupp', lookup)
            print(lookup[field], "%%")
        except KeyError:
            print('No matching key!!!', datasetkey)
        # dct=dict()
        dct['field'] = field
        dct['term'] = kword
        datasetkey = j['key']
        print("now dict --- ", dct)
            # try:
        print('after dataset_metadata_lookup loop/// ')
        try:
            res =  lookup[field]
        except KeyError:
            print('After lookup KEYERROR')
            continue
        print('RESS:  ', res)
        print('IS DICT??:  ', type(res))

        if isinstance(res, (dict)):
            print("IS A DICT() ")
            for j, k in res.items():
                # for f in field:
                    dct['field'] = f
                    print('"""field"""=', f)
                    dct['term'] = kword
                    print('TTTYPE :: ', type(j))
                    dct['meta_content'] = res
                    print('##key ', j)
                    if isinstance(k, (list)):
                        print('¤¤¤WE HAVE A LIST¤¤¤')

                        # words = k.split(' ')
                        # print(type(words))
                        dd = test_distance(k, kword, dct, datasetkey)
                        # g.update(dd)
                        # print('GGG', g)
                        retlist.append(dd)
                    else:
                        words = k.split(' ')
                        for w in words:
                            cc = test_distance(w, kword, dct, datasetkey)
                            retlist.append(cc)
                            # print('GGG', g)

            # return g
        else:
            print("STRING TO LIST...")
            splitres = res.split()
            print(splitres)
            for word in splitres:
                dct['field'] = f
                dct['term'] = kword
                dct['meta_content'] = res
                g = test_distance(word, kword, dct, datasetkey)
                print(word, g)
                if g:
                    print('orig returnlist!!!', retlist)
                    retlist.append(copy.copy(g))
                    print('RETURNLIST:::', retlist)
    # print(type(g), 'WHAT IS G????')
    print('RETURNLIST:::', retlist)
    return retlist
    #     except:
    #         print('No matching key!!!')
    #         print(datasetkey)
    #         print('The field {} was not found.'.format(field))
    # # except AttributeError:
    # else:
    #     print('The field {} was not found.'.format(field))


# rr = gbif_api('http://api.gbif.org/v1/dataset/', '5d784d06-fa1d-4f00-8cdc-663d04d26061')
# print(rr['doi'])

# res = terms_lookup('LTER', search_url, dframe, 'description')
distilled = dframe
for f in fields:
    for t in terms:
        res = dataset_api_search(search_url, t, f)
        print('BEGIN LOOP ==== ', res)
        res = filter(None, res)
        # distilled = distilled.append(res, ignore_index=True)
        distilled = pd.DataFrame.from_records(res, index='datasetkey')
print(distilled.to_string())

directory = 'C:/Users/jlegind/PycharmProjects/sample_protocols/'
file = 'sampleevent.csv'
distilled.to_csv(os.path.join(directory, file))
#
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