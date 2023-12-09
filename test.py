# import torch
# x = torch.rand(5,3)
# print(x)
# print(torch.cuda.is_available())

import benepar, spacy

nlp = spacy.load('en_core_web_md')
if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})
doc = nlp("The time for action is now. It's never too late to do something.")
sent = list(doc.sents)[0]
print(sent._.parse_string)
sent._.labels
print(list(sent._.children)[0])