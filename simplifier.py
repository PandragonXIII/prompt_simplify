import spacy
import warnings
import en_core_web_sm
# import benepar

'''
a simplifier class that takes in a sentence and returns a simplified sentence
by constructing a parse tree and search from the root to noun nodes.
'''
class Simplifier:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm') # load spacy model
        self.nlp.add_pipe(self.nlp.create_pipe('


nlp = spacy.load('en_core_web_md')
nlp.add_pipe("benepar", config={"model": "benepar_en3"})
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # doc = nlp("Seeking tghbh into the organization or composition of //'s predicted test model.")
    doc = nlp("li says : ' hello!'")
    # doc = nlp("The time for action is now. It's never too late to do something.")
sent = list(doc.sents)[0]
print(sent._.parse_string)
sent._.labels
print(list(sent._.children)[0])