import spacy
import warnings
# import benepar

'''
a simplifier class that takes in a sentence and returns a simplified sentence
by constructing a parse tree and search from the root to noun nodes.
'''
class Simplifier:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm') # load spacy model
        self.blacklist = [] # a list of words we donnot need
        self.whitelist = ['NOUN', ] # a list of words we stop at


    def simplify(self, sentence):
        doc = self.nlp(sentence)
        sent = list(doc.sents)[0]
        root = sent.root
        stack = []
        stack.append(root)

        preserved = []
        while stack.__len__() > 0:
            node = stack.pop()
            preserved.append(node.i)

            if node.pos_ in self.whitelist:
                print("preserved: ", node.text)
                continue # stop at noun nodes
            for child in node.children: # otherwise add children to stack
                stack.append(child)

        preserved.sort()
        print (preserved)
        for idx in preserved:
            print(doc[idx].text, end=" ")
        print(".")

    def show_tree(self, sentence):
        doc = self.nlp(sentence)
        sent = list(doc.sents)[0]
        for token in sent:
            print(token.text, token.pos_, token.head)


        # print(type(sent[0]))
        # print([(w.text, w.pos_) for w in sent])


simp = Simplifier()
simp.simplify("Seeking insight into the organization or composition of Duolingo's predicted test model.")
# simp.show_tree("Seeking insight into the organization or composition of Duolingo's predicted test model.")


# nlp = spacy.load('en_core_web_md')
# nlp.add_pipe("benepar", config={"model": "benepar_en3"})
# with warnings.catch_warnings():
#     warnings.simplefilter("ignore")
#     # doc = nlp("Seeking tghbh into the organization or composition of //'s predicted test model.")
#     doc = nlp("li says : ' hello!'")
#     # doc = nlp("The time for action is now. It's never too late to do something.")
# sent = list(doc.sents)[0]
# print(sent._.parse_string)
# sent._.labels
# print(list(sent._.children)[0])