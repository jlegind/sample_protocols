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

protocols = ['sampling','trap','transect','plot','survey','netting','census','trawl']
shoulds = []
for term in protocols:
    should = {
              "match_phrase": {
                "description": term
              }
            }
    shoulds.append(should)

# print(shoulds)
conditions = shoulds

payload = {
  "_source": {
		"includes": ["title", "description", "_score"],
		"excludes": ["geographicCoverages", "samplingDescription.sampling"]
	}
	,
    "size": 2010,
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

def highlight(txt, pattern):
    print('txt =={} \n and pattern : {}'.format(txt, pattern))
    matched = []
    # fields = ['title', 'description']
    fields = ['description']
    print('txt type is : ', type(txt), '  ', txt)
    print(txt)
    item_list = [txt[x] for x in fields]
    item_list_conc = item_list[0]\
                     # +item_list[1]
    one_list = '. '.join(item_list_conc)
    print('ITEM LIST here = ',len(one_list), type(one_list), one_list)
    # item_list.append(item)
    # print('item list len:{}'.format(len(item_list)), item_list[0])
    # print('item list 0 {}'.format(item_list[0]))
    # for matchedtext in one_list:
    print('mathcedetexxxxxtttt: len: {} + text: {}'.format(len(one_list), one_list))
    hit = re.findall(pattern, one_list)
    print('#hit##', hit)
    matched.append(hit)
    print('type matched?? : ', type(matched), matched)
    res = set(matched[0])
    return res

with open(dir+'/multi.csv', 'w', newline='', encoding='utf-8') as sample_event_file:
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

            highs = []

            # highs.append(hl)
            # matched = []
            # for matchedtext in re.findall(r'(?<=<em class="gbifHl">).*?(?=</em>)', description):
            #     matched.append(matchedtext)
            # terms = list(set(matched))
            # print('t#e#r#m#s# :: ', hl)
            # samplingDescription = replace_pt.sub("", samplingDescription)
        except KeyError as e:
            print('keyerror ¤¤¤¤¤¤¤¤')
            print(e)
            continue

        # if datasetkey == 'e567684d-9998-4604-9790-b0ac00e090c1':
        #     print('desc#####: ', description)
        #     break

        # singlerow.extend([title, description, samplingDescription, score])
        # rows.append(singlerow)
        # ll = len(description)
    #
    # hit = extract_values(res, '_source')[0]
    #     print('datasetkey:{}\n title:{}\ndesc: {}\nsampling: {}\n protocol={}\nscore={}'.format(datasetkey, title,description,samplingDescription,hl,score))
        # print(rows)
        # break
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