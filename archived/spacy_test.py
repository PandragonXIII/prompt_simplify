# import torch
# x = torch.rand(5,3)
# print(x)
# print(torch.cuda.is_available())

import benepar, spacy
import warnings
nlp = spacy.load('en_core_web_md')
nlp.add_pipe("benepar", config={"model": "benepar_en3"})
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    doc = nlp("I bought two pieces of cake.")
    # doc = nlp("The time for action is now. It's never too late to do something.")
for token in doc:
    print(token.text, token.pos_, token.tag_, )
sent = list(doc.sents)[0]
print(sent._.parse_string)
# sent._.labels
# print(list(sent._.children)[0])