from elasticsearch6 import Elasticsearch
from json_extractor import extract_values
from bs4 import BeautifulSoup
import csv
import json
from collections import Counter
import re


es = Elasticsearch(
["http://c3n1.gbif.org:9200/dataset/", "localhost:9200"])
# print(es.info())

def srch(body):
    res = es.search(index="dataset", _source = ["title", "description", "_score", "samplingDescription.sampling"], _source_excludes = ["geographicCoverages"], body=body)
                    # filter_path=['hits.hits._id', 'hits.hits._type'], body=body)

    return res

protocols = ['sampling','trap','transect','plot','survey', 'surveys','netting','census','trawl']

def condition(terms):
    '''
    Returns a construct of multiple 'should' conditions
    :param terms: in our case a list of sample event/protocol terms
    :return: the construct to be inserted into the payload body
    '''
    shoulds = []
    for term in protocols:
        should = {
                  "match_phrase": {
                    "description": term
                  }
                }
        shoulds.append(should)
    return shoulds
# print(shoulds)
conditions = condition(protocols)

payload = {
  "_source": {
		"includes": ["title", "description", "_score"],
		"excludes": ["geographicCoverages", "samplingDescription.sampling"]
	}
	,
    "size": 2000,
  "query" : {
    "bool": {
      "should":
        conditions
    }
  },
  "highlight": {
"pre_tags": [
"<em class=\"gbifHl\">"
],
"post_tags": [
"</em>"
],
"type": "plain",
"force_source": True,
"require_field_match": False,
"encoder": "html",
"number_of_fragments": 0,
"fields": {
"title": {},
"description": {}

}
}
}
print(payload)
res = srch(payload)
# print(res)
ore = res['hits']['hits']
# print('ORE ---', type(ore), ore)
# print(ore)
# samplingDescription = ''
rows = []
dir = r'C:/Users/bxq762/Dropbox/Sample event/'
# tabfile = open(dir+'braunblanquet.csv', mode="w")
# tag_writer = csv.writer(tabfile, delimiter='\t')
def clean(term):
    #For cleaning html and linebreaks from text strings
    #Good for keyword and free text fields
    soup = BeautifulSoup(term, features="html.parser")
    res = soup.get_text()
    tmp = res.split()
    cleaned = ' '.join(tmp)
    cleaned = cleaned.strip('\r\n')
    return cleaned
# pattern = '[\{\}]'
# replace_pt = re.compile(pattern)

def highlight(txt, pattern):
    '''
    Gets the results of the highlighted text.
    :param txt: text to be searched
    :param pattern: regex pattern
    :return: a list of terms that were matched for a particular string
    '''
    print('txt =={} \n and pattern : {}'.format(txt, pattern))
    matched = []

    fields = ['description']
    print('txt type is : ', type(txt), '  ', txt)
    print(txt)
    item_list = [txt[x] for x in fields]
    item_list_conc = item_list[0]
    one_list = '. '.join(item_list_conc)
    print('ITEM LIST here = ',len(one_list), type(one_list), one_list)

    print('mathced texxxxxtttt: len: {} + text: {}'.format(len(one_list), one_list))
    hit = re.findall(pattern, one_list)
    hit = [x.lower() for x in hit]
    print('#hit##', hit)
    matched.append(hit)
    print('type matched?? : ', type(matched), matched)

    res = list(set(matched[0]))
    #Set returns a unique 'set' which must be cast as list
    return res

#write a function taking dir+name + fieldnames list
with open(dir+'/multi_test.csv', 'w', newline='', encoding='utf-8') as sample_event_file:
    fieldnames = ['datasetkey', 'title', 'description', 'protocol_terms', 'score']
    writer = csv.DictWriter(sample_event_file, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    for gold in ore:
        print('gold ### =',type(gold), gold)
        # singlerow = []
        datasetkey = gold['_id']
        score = gold['_score']
        gold_source= gold['_source']
        # print('##SOURCE', gold['_source'])
        title = gold_source['title']
        title = title.strip('\r\n')
        description = gold_source['description']
        description_cleaned = clean(description)
        title = clean(title)
        term_lights = [1]
        print("#TITLE ::: ", title)
        print('##desc##: ', description_cleaned)
        high = gold['highlight']
        pattern = r'(?<=<em class="gbifHl">).*?(?=</em>)'

        print('!!!highlight!!! : ', high)
        terms = highlight(high, pattern)
        print('ttterms : ', terms)
        print(json.dumps(term_lights, indent=2), type(gold))
        # print('##highlight : ', term_lights , '\ntype : ', type(term_lights) )
        print('type orig description: ', type(description))
        print('going to write: datasetkey: {}, title: {}, description: {}, protocol_terms: {}, score: {} '.format(
            datasetkey, title, description_cleaned, high, score))
        writer.writerow(
            {'datasetkey': datasetkey, 'title': title, 'description': description_cleaned, 'protocol_terms': terms,
             'score': score})
        try:

            # hl = highlight(gold, pattern, ['highlight', 'description'])
            # print('HIGHLIGHT¤¤¤¤¤:', hl)

            samplingDescription = gold_source['samplingDescription.sampling']['sampling']
            if samplingDescription:
                samplingDescription = clean(samplingDescription)
                print(type(samplingDescription))

        except KeyError as e:
            print('keyerror ¤¤¤¤¤¤¤¤')
            print(e)
            continue

dkeys_list = []
def predominant_sign(data):
    signs = Counter(k['_id'] for k in data if k.get('_id'))
    for sign, count in signs.most_common():
        # print(sign, count)
        dkeys_list.append(sign)

with open('ore.txt', 'w', encoding='utf-8') as flie:
    writer = flie.write(str(ore))

tally = predominant_sign(ore)
print('key list == ', dkeys_list)
uniq = set(dkeys_list)
print('NUMBER of datasets with term = ', len(dkeys_list))
print('length unique keys:: ', len(uniq))