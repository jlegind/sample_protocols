import requests

#get content of one json field

search_url = 'http://api.gbif.org/v1/dataset/'


def field_lookup(datasetkey, field, api=search_url):

    surl = api+'{}'.format(datasetkey)
    response = requests.get(surl)
    rson = response.json()
    print(rson)
    datasettitle = rson[field]
    return datasettitle



