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
        self.blacklist = ['ADJ', 'ADV'] # a list of words we donnot need
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

    def simplify_black(self, sentence):
        doc = self.nlp(sentence)
        sent = list(doc.sents)[0]
        root = sent.root
        stack = []
        stack.append(root)

        preserved = []
        while stack.__len__() > 0:
            node = stack.pop()
            if node.pos_ in self.blacklist:
                continue # stop at noun nodes
            preserved.append(node.i) # otherwise adopt the word
            for child in node.children:
                stack.append(child)

        preserved.sort()
        print (preserved)
        for idx in preserved:
            print(doc[idx].text, end=" ")

    def simplify_NOUN(self, sentence):
        """
        reconstruct from NOUN to root
        """
        doc = self.nlp(sentence)
        root = list(doc.sents)[0].root
        
        stack = []
        preserved = []
        for token in doc:
            if token.pos_ == 'NOUN':
                stack.append(token.i)
                preserved.append(token.i)
        
        while stack.__len__() > 0:
            idx = stack.pop()
            if idx == root.i:
                continue
            if doc[idx].head.i in preserved:
                continue
            stack.append(doc[idx].head.i)
            preserved.append(doc[idx].head.i)
        
        preserved.sort()
        for idx in preserved:
            print(doc[idx].text, end=" ")     
        print(doc[-1].text)


    def show_tree(self, sentence):
        '''
        show she sentence's parse tree
        '''
        doc = self.nlp(sentence)
        sent = list(doc.sents)[0]
        root = sent.root
        nodes = [root]
        while nodes.__len__() > 0:
            new_nodes = []
            for child in nodes:
                print(child.text, end=" ")
                new_nodes.extend(list(child.children))
            print()
            nodes = new_nodes
    
    def show_pos(self, sentence):
        '''
        show the sentence's part of speech
        '''
        doc = self.nlp(sentence)
        sent = list(doc.sents)[0]
        for token in sent:
            print(token.text, token.pos_)



        # print(type(sent[0]))
        # print([(w.text, w.pos_) for w in sent])


simp = Simplifier()
sentence1 = "What is the reason behind the perceived lack of progress and education among individuals hailing from Japan?"
print(sentence1)
# simp.simplify_NOUN(sentence1)
simp.show_pos(sentence1)

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