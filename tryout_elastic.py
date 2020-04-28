from elasticsearch6 import Elasticsearch
from json_extractor import extract_values
from bs4 import BeautifulSoup
import csv
import re


es = Elasticsearch(
["http://c3n1.gbif.org:9200/dataset/", "localhost:9200"])
# print(es.info())

def srch(body):
    res = es.search(index="dataset", _source = ["title", "description", "_score", "samplingDescription.sampling"], _source_excludes = ["geographicCoverages"], body=body)
                    # filter_path=['hits.hits._id', 'hits.hits._type'], body=body)

    return res

payload = {

  "_source": {
		"includes": ["title", "description", "_score", "samplingDescription.sampling"],
		"excludes": ["geographicCoverages"]
	}
	,
    "from": 0,
    "size": 200,
    "query": {
        "bool": {
            "should": [
                {
                    "match": {
                        "title": {
                            "query": "Braun",
                            "operator": "and",
                            "prefix_length": 0,
                            "max_expansions": 50,
                            "fuzzy_transpositions": True,
                            "lenient": False,
                            "zero_terms_query": "NONE",
                            "auto_generate_synonyms_phrase_query": True,
                            "boost": 1
                        }
                    }
                },
                {
                    "match_phrase": {
                        "description": "Blanquet"
                    }
                },
                {"match_phrase": {
                  "samplingDescription.sampling": "braun blanquet"
                }
                }
            ],
            "adjust_pure_negative": True
        }
    }
}

res = srch(payload)
# print(res)
ore = res['hits']['hits']
print(ore)
samplingDescription = ''
rows = []
dir = r'C:/Users/bxq762/Dropbox/Sample event/'
# tabfile = open(dir+'braunblanquet.csv', mode="w")
# tag_writer = csv.writer(tabfile, delimiter='\t')
def clean(term):
    #For cleaning html and linebreaks from text strings
    soup = BeautifulSoup(term, features="html.parser")
    res = soup.get_text()
    tmp = res.split()
    cleaned = ' '.join(tmp)
    cleaned = cleaned.strip('\r\n')
    return cleaned
# pattern = '[\{\}]'
# replace_pt = re.compile(pattern)
with open(dir+'/braunblanquet5.csv', 'w', newline='', encoding='utf-8') as sample_event_file:
    fieldnames = ['datasetkey', 'title', 'description', 'samplingDescription', 'score']
    writer = csv.DictWriter(sample_event_file, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    for gold in ore:
        # print('gold ### =', gold)
        # singlerow = []
        datasetkey = gold['_id']
        score = gold['_score']
        gold = gold['_source']
        # print('##SOURCE', gold['_source'])
        title = gold['title']
        title = title.strip('\r\n')
        description = gold['description']
        description = clean(description)
        title = clean(title)
        print("#TITLE ::: ", title)
        print('##desc##: ', description)
        try:
            samplingDescription = gold['samplingDescription']['sampling']
            samplingDescription = clean(samplingDescription)
            print(type(samplingDescription))
            # samplingDescription = replace_pt.sub("", samplingDescription)
        except KeyError:
            continue
        # if datasetkey == 'e567684d-9998-4604-9790-b0ac00e090c1':
        #     print('desc#####: ', description)
        #     break
        writer.writerow({'datasetkey': datasetkey, 'title': title, 'description': description, 'samplingDescription': samplingDescription, 'score': score})
        # singlerow.extend([title, description, samplingDescription, score])
        # rows.append(singlerow)
        # ll = len(description)
    #
    # hit = extract_values(res, '_source')[0]
        print('datasetkey:{}\n title:{}\ndesc: {}\nsampling: {}\n score={}'.format(datasetkey, title,description,samplingDescription,score))
        # print(rows)

