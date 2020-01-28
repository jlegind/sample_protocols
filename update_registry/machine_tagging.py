import change_registry_using_API as chapi
import os
import csv
import pandas
import math
from tabulate import tabulate

dir = r"C:\Users\jlegind\Dropbox\Sample event"
# with open(dir+'\lter_dafor.csv', encoding="utf8") as cf:
#     creader = csv.reader(cf, delimiter='\t')
#     for row in creader:
#         print(row)

data = pandas.read_csv(dir+'/lter_dafor_comment.csv')
print(data.columns.values)
data = data.dropna(subset=['term'])

# print(data['datasetkey'].to_string())
data = data.loc[data['status'] != 'FALSE']
data = data[['datasetkey', 'comment', 'term']]
data = data.drop_duplicates(keep='first')
print(data.to_string())
# setkeys = set(data)

ddata = data.to_dict('records')
# print(ddata)

chapi.delete_machineTag_from_namespace('1683e434-321c-4b55-a5b0-6e05eb6d931f', 'gbif.org', 'jlegind', 'mussimus')
# print(set(ddata))
for j in ddata:
    # print(type(j['comment']), j['comment'])
    try:
        if math.isnan(j['comment']):
            # print('tagging dataset ', j['datasetkey'])
            tag = {'protocol':j['term']}
            print(tag)
            # chapi.add_machineTag(j['datasetkey'], 'gbif.org', 'sampling event', j['term'],
            #                      'jlegind', 'mussimus')
            break
        else:
            # print('tagging dataset ', j['datasetkey'], j['comment'])
            tag = {'protocol':j['term'], 'comment':j['comment']}

    except TypeError:
        tag = {'protocol': j['term'], 'comment': j['comment']}

        print('tagging dataset in except: ', tag)
# print(tabulate(data, tablefmt='psql'))

# chapi.add_machineTag('1683e434-321c-4b55-a5b0-6e05eb6d931f', 'gbif.org', 'sampling protocol', 'LTER', 'jlegind', 'mussimus')

