import nltk
import requests
import copy
import pandas as pd
import responses
import os

search_url = 'http://api.gbif.org/v1/dataset/search?q='
# terms = ['LTER', 'DAFOR', 'transect', 'quadrat', 'census', 'drones', 'field work']
terms = ['lter']
# terms = ['dafor']
# cols = ['field', 'term', 'datasetkey', 'accurates', 'close-enough', 'distance', 'number']
# dframe = pd.DataFrame(columns=cols)
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

def isstring(word, term, field, datasetkey):
    print('isstrterm: ', term)
    # res = remove_chars(rson)
    # print('lenres = ', len(res))
    # print(res)
    sendback = list()
    # for word in rson:
    # print(word)
    feedback = test_distance(word, term, field, datasetkey)
    print('feed -- ', feedback)
    if feedback:
        # print('feedback is real ?!?!')
        sendback.append(feedback)

    print('sendback: ', sendback)
    if sendback:
        lsb = len(sendback)
        print('sb not none: ', lsb, sendback)
        if lsb ==1:
            sendback = sendback[0]
        return sendback

def remove_chars(words):
    #Must have string param
    print('remover {} and type {}:'.format(words, type(words)))
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

    if isinstance(word, (list))== False:
        word = word.lower()

    print(word, kword, field, "######test_distance##")

    rt = list()
    dist = nltk.edit_distance(kword, word)
    print('* ',word, dist, ' *')
    if dist == 1:

        print("--success--close\n ", word)
        # close_pair = (kword, word, dist, field, datasetkey)
        tmp = [kword, word, dist, field, datasetkey]
        for j in tmp:
            print('elem: ', j)
            rt.append(j)
        # rt.append(acc_pair)
        print('close pair: ', tmp)
        # rt.append(tmp)
        # return close_pair

    elif dist == 0:

        print("--success--accurate\n ", word)
        acc_pair = [kword, word, dist, field, datasetkey]
        for j in acc_pair:
            # print('elem: ', j)
            rt.append(j)
        # rt.append(acc_pair)
        print('acc pair: ', acc_pair)
        # rt.append(acc_pair)
        # print('acc pair: ', acc_pair)
        # return acc_pair
    if rt:
        print('rt ', rt)
        return rt
    else:
        print('none rt ', rt)



def parsxson(xson, term, field, datasetkey, sender=list()):
    # xson = xson[field]

    # sender = list()
    def strpars(sentence):
        words = remove_chars(sentence)
        print('in stringif ', term, words)
        for w in words:
            res = isstring(w, term, field, datasetkey)

            if res is not None:
                print('string res:: ', res)

                return res

    if isinstance(xson, str):
        print('in instancestr')
        rstr = strpars(xson)
        if rstr is not None:
            rstr.append(xson)
        return rstr
    # sender = list()
    if isinstance(xson, (dict)):
        print('isDict()')
        # sender = list()
        for k, val in xson.items():
            # print(k, 'and type: ', type(k))
            print('Field k ', k, val)
            # RECURSIVE ---------
            if isinstance(val, (dict)):
                print('val is dict', val)
                parsxson(val, term, field, datasetkey, sender=sender)
            # parson(son[k], )
            # if k[0] != field:

            print('!type: ', type(val), val)
            if isinstance(val, list):
                print('RECURSIVE LIST')
                for j in val:
                    oput = parsxson(j, term, field, datasetkey)
                    print('oput: ', oput)
                    sender.append(oput)
                    print('sender oput: ', sender)
                    # return oput
            if isinstance(val, str):

                print('val is -string-', val)
                sent = strpars(val)
                print('sent is now:: ', sent)
                if sent:
                    sent.append(val)
                    sender.append(sent)
                    print('not none val: ', val)
                    print('not none: ', sent)

                # seli = list()
                # seli.append(sent)
                # sender.append(sent)
                if sender:
                    print('sender;; ', sender)
                    return sender

# elif isinstance(xson, (str)):
#     print('NOT DICT - maybe string? ', type(xson))
#     print('string term and key', term, datasetkey)
#     words = remove_chars(val)
#     # res = ''
#     for w in words:
#         res = isstring(w, term, field, datasetkey)
#         print('parson res tuple: ', res)
#         if res is not None:
#             print('reaches return - ', res)
#             return res
#         else:
#             print('none res : ', res)
#
#         else:
#             print('LIST -- maybe do something about that ', val)

search_url = 'http://api.gbif.org/v1/dataset/search?q='

#A break pad !!!
limiter = 20

# thedct = {"accurate":{'term': '', 'field': '', 'number': 0, 'datasetkey': '', 'accurates': '', 'distance': None},
#           "close_dict":{'term': '', 'field': '', 'number': 0, 'datasetkey': '', 'accurates': '', 'distance': None}}
#-------------------------useful BELOW --------------------------------------
# d_list = []
dflist = list()
for t in terms:
    for f in fields:
        res = term_api_search(search_url, t)
        print('len json api search: ', len(res))
        ct = 0
        # if dsets is not None:
        for j in res['results']:
                ct += 1
                if ct > limiter:
                    print('breaking at : ', ct)
                    break
                # print(j)
                print('jkey', j['key'])
                # dsets.append(j['key'])
                datasetkey = j['key']

        dsets = list()
        if dsets is not None:
            for j in res['results']:
                ct += 1
                if ct > limiter:
                    print('breaking at : ', ct)
                    break
                # print(j)
                # print('jkey', j['key'])
                dsets.append(j['key'])
        diter = iter(dsets)
        while True:
            try:
                datasetkey = next(diter)
                print('jkey is : ', datasetkey)
                # print(dsets)
            # print('acute term list: {} - key {}'.format(terms, datasetkey))
            # for f in fields:
                lookup = dataset_metadata_lookup(datasetkey, f)
                print('lookup! :', f, lookup)
                x = parsxson(lookup, t, f, datasetkey)
                print('pars is ==', x)
                if x is not None:
                    dflist.append(x)
                print('current dflist: ', dflist)
            except StopIteration:
                print('iter end!!!!')
                break


cols = ['term', 'target-word', 'distance', 'json field', 'datasetkey', 'context']
print('dflist : : ', dflist)

df = pd.DataFrame(dflist, columns=cols)
print(df.to_string())


                #     # newdct = {}
                #     print('term and key: ', t, datasetkey)
            #     news = parson(lookup, t, f, datasetkey)
            #     print('type news: ', type(news))
            # #     print('str yield generator')
            #     print('this is it: ', news)
            #     if news:
            #         # print('news0', news[0])
            #         # for n in news:
            #         #     n.append(lookup)
            #         #     print('newscomponent: ', n)
            #         # n.append(lookup)
            #         for j in news:
            #             j.append(lookup)
            #             d_list.append(j)
            # except StopIteration:
            #     break
# print('dsets', len(dsets), dsets)
# print('longlist: ', d_list)
# cols = ['term', 'target-word', 'distance', 'json field', 'datasetkey', 'context']
# final_df = pd.DataFrame(d_list, columns=cols)
# print(final_df.to_string())
#
# directory = 'C:/Users/jlegind/PycharmProjects/sample_protocols/'
# file = 'sampleevent.csv'
# final_df.to_csv(os.path.join(directory, file))