import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet
import csv
import spacy


# print(wordnet.synsets('lively'))
# print(wordnet.synset('lively.s.02').definition())
print(wordnet.synset('lively.s.02').lemma_names())

# load origin sentence from E:\research\prompt_simplify\data\jade_benchmark_en.csv
filename = 'E:\\research\\prompt_simplify\\data\\jade_benchmark_en.csv'
data = []
with open(filename, encoding='utf-8') as f:
    reader = csv.reader(f)
    header_row = next(reader)
    for row in reader:
        data.append(row[1])

result = []
nlp = spacy.load("en_core_web_sm")
doc = nlp(data[0])
sent = list(doc.sents)[0]
temp = 0
for i in range(len(sent)):
    token = sent[i]
    result.append(token.text)
    print(token.text, token.pos_)
    # choose a token to replace
    if token.pos_ == 'NOUN':
        # find the word's synsets
        synsets = wordnet.synsets(token.text, pos=wordnet.NOUN)
        # print(synsets)
        # choose the first synset
        synset = synsets[0]
        print(synset)
        define = synset.definition()
        define = define.split(' ')
        # # choose the first lemma
        # lemma = synset.lemmas()[0]
        
        # print(lemma)
        # # get the lemma's name
        # lemma_name = lemma.name()
        # print(lemma_name)
        # store the new sentence in result
        result = result[:i+temp] + define + result[i+1+temp:]
        temp+=len(define)
print(result)


# # store result in data/result.csv
# with open('data/result.csv', 'w', newline='', encoding='utf-8') as f:
#     writer = csv.writer(f)
#     writer.writerow(['sentence', 'answer'])
#     for i in range(len(data)):
#         writer.writerow([data[i], result[i]])
