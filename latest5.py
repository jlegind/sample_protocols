import latest45 as lat
#
# ll = [1,2,4]
# ll= 'kjh'
# if isinstance(ll, (list)):
#     print('ll is list')
# elif  isinstance(ll, (str)):
#     print('is string')


# def isstring(word, term, field, datasetkey):
#     print('isstrterm: ', term)
#     # res = remove_chars(rson)
#     # print('lenres = ', len(res))
#     # print(res)
#     sendback = list()
#     # for word in rson:
#     # print(word)
#     feedback = test_distance(word, term, field, datasetkey)
#     print('feed -- ', feedback)
#     if feedback:
#         # print('feedback is real ?!?!')
#         sendback.append(feedback)
#
#     print('sendback: ', sendback)
#     if sendback:
#         print('sb not none: ', sendback)
#         return sendback

xson = {"samplingDescription": {
    "studyExtent": "The idea is to subsample about 3% of the land area of South Northumberland and Durham in 1km × 1km Ordnance Survey squares over three years.",
    "sampling": "The volunteer observers were asked to...\n1. Record all the species that they could identify confidently.\n2. Include, planted or sown plants where they are an important feature of the landscape, but to note when they are planted.\n3. To try to visit the full range of habitats within the grid square.\n4. When they had finished surveying the square, they were asked to assign a DAFOR letter to each species you found. The DAFOR scale is D = Dominant; A = Abundant, F = Frequent, O = Occasional, R = Rare.",
    "qualityControl": "Observations were digitised and reviewed by John Durkin, John O'Reily and Quentin Groom. Any obvious mistakes where deleted at this point.",
    "methodSteps": [
      "Observations were digitised using Mapmate (http://www.mapmate.co.uk/)."
    ]
  }}

def parsxson(xson, term, field, datasetkey):
    print(xson)
    sender = list()
    def strpars(sentence):
        words = lat.remove_chars(sentence)
        print('in stringif ', term, words)
        for w in words:
            res = lat.isstring(w, term, field, datasetkey)

            if res is not None:
                print('string res:: ', res)
                return res

    if isinstance(xson, str):
        rstr = strpars(xson)
        return rstr
    if isinstance(xson, (dict)):
        print('isDict()')

        for k, val in xson.items():
            # print(k, 'and type: ', type(k))
            print('Field ', k, val)
            #RECURSIVE ---------
            if isinstance(val, (dict)):
                print('val is dict', val)
                parsxson(val, term, field, datasetkey)
            # parson(son[k], )
            # if k[0] != field:

            print('!type: ', type(val))
            if isinstance(val, list):
                print('RECURSIVE LIST')
                for j in val:
                    # oput = parson(j, term, field, datasetkey)
                    print('oput: ', j)
                    # return oput
            if isinstance(val, str):
                print('val is -string-', val)
                sent = strpars(val)
                print('sent is now:: ', sent)
                if sent :
                    sent.append(val)
                    sender.append(sent)
                    print('not none val: ', val)
                    print('not none: ', sent)


                # seli = list()
                # seli.append(sent)
                # sender.append(sent)
                print('sender;; ', sender)
                yield sender
                # print('pre return sender: ', sender)
    # return sender

# parsxson(xson, 'dafor', 'samplingdescription', '5d784d06-fa1d-4f00-8cdc-663d04d26061')
# print('init: ', res)
# for j in res:
#     print('the res', j)
def myfunction():
    l = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    total = 0
    for i in l:
        if total < 6:
            yield i  #yields an item and saves function state
            total += 1
        else:
            break

g = myfunction()

for j in g:
    print(j)