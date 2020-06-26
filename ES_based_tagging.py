from update_registry import change_registry_using_API as chapi
import os
import csv
import pandas
import math


dir = r"C:\Users\bxq762\Dropbox\Sample event"
# with open(dir+'\lter_dafor.csv', encoding="utf8") as cf:
#     creader = csv.reader(cf, delimiter='\t')
#     for row in creader:
#         print(row)
fname = 'sample_event_terms.tsv'
path = '{}\{}'.format(dir, fname)
print(path)
data = pandas.read_csv(path, sep='\t', encoding='utf8')
print(data.columns.values)
# print(data.to_string())
# data = data.dropna(subset=['term'])

# print(data['datasetkey'].to_string())
# data = data.loc[data['status'] != 'FALSE']
# data = data[['datasetkey', 'comment', 'term']]
data = data.drop_duplicates(keep='first')
# print(data.to_string())
# data = data.iloc[[0]]
# print(data.to_string())
# setkeys = set(data)
# protocol = 'Braun Blanquet'

ddata = data.to_dict('records')
# print(ddata)
#
# # chapi.delete_machineTag_from_namespace('1683e434-321c-4b55-a5b0-6e05eb6d931f', 'gbif.org', 'jlegind', 'mussimus')
# # print(set(ddata))
for j in ddata:
    # print(type(j['comment']), j['comment'])
    print('this is J', j)
    dkey = j['datasetkey']
    name_ = 'samplingEvent'
    value = {"matchedTerms":j['protocol_terms'], "ElasticSearchScore":j['ElasticSearch_score']}
    print(dkey, name_, value)
    break
#     try:
#         # if math.isnan(j['comment']):
#             # print('tagging dataset ', j['datasetkey'])
#             tag = {'##########\nprotocol': protocol}
#             print(tag)
#             dkey = j['datasetkey']
#             print(dkey)
#             chapi.add_machineTag(dkey, 'gbif.org', 'sampling event', protocol,
#                                  'jlegind', 'mussimus', api="http://api.gbif.org/v1/dataset/")
#             # break
#         # else:
#             # print('tagging dataset ', j['datasetkey'], j['comment'])
#             # tag = {'protocol': protocol, 'comment':j['comment']}
#     # chapi.add_machineTag()
#
#     except TypeError:
#         tag = {'protocol': j['term'], 'comment': j['comment']}
#
#         print('tagging dataset in except: ', tag)
# print(tabulate(data, tablefmt='psql'))

# chapi.add_machineTag('1683e434-321c-4b55-a5b0-6e05eb6d931f', 'gbif.org', 'sampling protocol', 'LTER', 'jlegind', 'mussimus')
