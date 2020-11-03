import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import nltk
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
lemma = nltk.wordnet.WordNetLemmatizer()

dataset_description = "Insects from light trap (1992–2009), rooftop Zoological Museum, Copenhagen	Collecting of Lepidoptera and Coleoptera was carried out with an automatically working modified Robinson light trap, which was installed 17.5 m above ground at the roof of the Zoological Museum in Copenhagen, Denmark. The trap worked around 4,500 nights from April to November during the years 1992 to 2009, and was emptied on an approximately weekly basis." \
                      " An analysis of this dataset was recently published in the Journal of Animal Ecology: https://dx.doi.org/10.1111/1365-2656.12452 The original data was deposited in Dryad and has now been republished in the standard Darwin Core Archive format using the IPT. Also note that the Lepidoptera data underwent a number of minor name corrections. Since new collaborations are extremely valuable to make the most of the data, researchers are encouraged to contact the dataset creator to collaborate on joint analyses and meta-analyses."
keyword = 'trap'
noPreceding = 3
cont_ = '0,{}'.format(noPreceding)
# newregx = rf"((\S+\s+){{{cont_}}}\b"+re.escape(pt)+r")"
#
# print(newregx)
# found = re.findall(newregx, dataset_description)
# print("fo u n d == ", found)
# patt = re.compile('((\w+ ){2})foreign currency')


def remove_stopWords(wordText, custom_stop):
    words = word_tokenize(wordText)
    print('IN remove_stopwords')
    stop = set(stopwords.words('english'))
    stopped_words = [word.lower() for word in words if word.isalnum()]
    print('first stoppped :::', stopped_words)
    stopped_words = [word for word in stopped_words if word not in stop]

    # print(type(stopped_words), stopped_words)
    return stopped_words
    # words = word_tokenize(stopped_text)
    # filtered = [word for word in stopped_words if word not in custom_stop]
    # return filtered

def pick_term_and_precedents(datasetkey, keyword, precedents='{0,2}'):
    outList = []

    cont_ = precedents
    print(type(cont_), cont_, '**********')

    newregx = rf"((\S+\s+){precedents}\b"+re.escape(keyword)+r")"
    # pp = rf"\s{{{cont_}}}"
    print(newregx)
    found = re.findall(newregx, dataset_description)
    print("fo u n d == ", found)
    # myregx = r"((\S+\W){"+re.escape(str(precedents))+r"}"+re.escape(keyword)+r")"
    stopped_text = remove_stopWords(dataset_description, [])

    print(stopped_text)
    stpd = ' '.join(stopped_text)
    print('stopped text |||', stpd)
    found = re.findall(newregx, stpd)
    print('findall == ', found)
    for j in found:
        outDict = {'datasetkey': datasetkey, 'keyword_preceding-word': '', 'context_keyword': ''}
        print(type(j), j)
        print(j[0])
        print('findall + keyword== ', j[1]+keyword)
        prec_word = j[1]
        context_keyword= j[0]
        outDict['keyword_preceding-word']=prec_word
        outDict['context_keyword'] = context_keyword
        print('context + keyword== ', j[0])
        outList.append(outDict)
    return outList

res = pick_term_and_precedents('fgsdfdds', 'trap')

print(res)

def lemmatizer(text):
    word_list = word_tokenize(text)
    lemmy = [lemma.lemmatize(w) for w in word_list]
    lem = ' '.join(lemmy)
    return lem
# trap = 'traps' = lemma.lemmatize(trap)
trap = lemmatizer(dataset_description)
camel = lemmatizer("wasn't")

print('traps = {} -\n camels = {}'.format(trap, camel))
txt = "modified Robinson light traps"
sb = re.sub(keyword, keyword.upper(), txt)
print(sb)
#
# pos = dataset_description.find('trap', 0, len(dataset_description))
# print(pos)
# tk = word_tokenize(dataset_description)
# words = [word.lower() for word in tk if word.isalnum()]
#
# print(tk)
# print(words)
#
# print('test spliot pos: ', dataset_description[:3].split())
#
# pos = [n for (n, e) in enumerate(words) if e == keyword]
#
# print(pos)
#
# for j in pos:
#     hit5 = dataset_description[:j].split()[-1:]
#     print(hit5)