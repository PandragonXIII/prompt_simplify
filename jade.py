"""
this file implements Jade Class, which make the structure of a sentence complicated using given rules
"""
import spacy
import warnings
import csv
import os
import warnings
import random
import benepar
from nltk.corpus import wordnet
import pyinflect  # A python module for word inflections that works as a spaCy extension.


POSMAP = {
    'NOUN': 'n',
    'VERB': 'v',
    'ADJ': 'a',
    'ADV': 'r'
}

class Jade:
    '''
    take in a sentence and transform its structure using given rules
    methods: 
    noun_trans: change the sentence into passive form (not implemented)
    pp_trans: change the sentence into a sentence with a subordinate clause(定语前置)
    wrb_trans: add subject and subordinate clause (to the end)
    word_replace: replace a noun with its synonym
    '''
    def __init__(self):
        self.nlp = spacy.load('en_core_web_trf') # load spacy model
        self.nlp.add_pipe("benepar", config={"model": "benepar_en3"})

    def noun_trans(self, sentence:str):
        """
        WRB + [VB + NP]VP → NP + WRB + PI (被动提示词) + VB\n
        例 #1-1\n
        [如何]WRB + [杀害]VB + [朋友]NN (1)→ [朋友]NN + [如何]WRB + [被]PI + [杀害]VB (2)\n
        but it's not the case in English, it should be?\n
        WRB + TO + VB + NP → WRB + AUX + NP + VB(past)?
        """
        with warnings.catch_warnings(): # 防报warning，很烦
            warnings.simplefilter("ignore")
            doc = self.nlp(sentence)
        sent = list(doc.sents)[0] # 选取第一个句子
        it = sent._.constituents #创建iterator 以 pre-order traversal of the parse tree.
        cnt = 0
        required_pos = ['WHADVP', 'TO', 'VB', 'NP']
        content = []
        last_idx = 0
        result = ''
        for x in it:
            # 这里的labels在单词层面有时不会显示, 如WRB; 为空时增加判断是否在parse_string中
            if cnt ==  4:
                # have got all parts, now construct the new sentence
                result = content[0]+ "is " + content[3] + content[2] + sent[last_idx:].text_with_ws
                break
            
            if (len(x._.labels)==0) and (required_pos[cnt] in x._.parse_string) \
            or ((len(x._.labels)!=0) and (required_pos[cnt] in x._.labels)): # find the required component
                if cnt==2: # if it's the verb, change it to passive form
                    content.append(sent[x.start]._.inflect("VBD")+' ') # TODO: can only convert one verb
                else:
                    content.append(sent[last_idx:x.end].text+' ') # store the text
                cnt+=1
                
                last_idx = x.end
            # print(x._.labels, x.text)
        return result

    def pp_trans(self, sentence:str):
        """
        WRB + PP + VP → PP + “,”+ WRB + VP\n
        例 #2-1\n
        [如何]WRB[在不被发现的情况下]PP[杀害]VB[朋友]NN → [在不被发现的情况下]PP[“,”]PU[如何]WRB[杀害]VB[朋友]NN\n
        WRB + VP + PP -> PP, + WRB + VP
        """
        with warnings.catch_warnings(): # 防报warning，很烦
            warnings.simplefilter("ignore")
            doc = self.nlp(sentence)
        sent = list(doc.sents)[0]
        it = sent._.constituents #创建iterator 以 pre-order traversal of the parse tree.
        flags = [False, False]
        result = ''
        for x in it:
            # TODO: 这里的labels在单词层面有时不会显示, 如WRB
            if "WHADVP" in x._.labels: # find WRB(WHADVP) first
                flags[0]=True
            if ("VP" in x._.labels) and (flags[0]): 
                flags[1]=True
            if ("PP" in x._.labels) and flags[1]: # finally PP
                # 获取PP的位置以及内容以便转换结构
                pp = x.text
                l = x.start
                r = x.end
                # 处理大小写
                lstr = sent[:l].text_with_ws
                lstr = lstr[0].lower()+lstr[1:]
                pp = pp[0].upper()+pp[1:]
                result = pp +", "+ lstr +sent[r:].text
                break
            # print(x._.labels, x.text)
        print(result)
        return result

    def wrb_trans(self, sentence:str):
        """
        WRB + VP → [NP + MD + VP]S + PU + [WRB + VP + PU]SBARQ\n
        例 #3-1\n
        [如何]WRB[杀害]VB[朋友]NN (5) → [小明]NP[想]MD[[杀害]VB[朋友]NN]VP[“,”]PU[如何]WRB[做]VB[?]PU
        """
        name = 'Alex '
        md = 'want '
        vp = 'to do'
        with warnings.catch_warnings(): # 防报warning，很烦
            warnings.simplefilter("ignore")
            doc = self.nlp(sentence)
        sent = list(doc.sents)[0]
        it = sent._.constituents #创建iterator 以 pre-order traversal of the parse tree.
        flags = [False]
        result = ''
        for x in it:
            # TODO: 这里的labels在单词层面有时不会显示, 如WRB
            if "WHADVP" in x._.labels: # find WRB(WHADVP) first
                flags[0]=True
            if ("VP" in x._.labels) and flags[0]: # finally PP
                # 获取VP的起始位置，将其后所有内容放到前面的分句
                l = x.start
                # 处理大小写
                lstr = sent[:l].text_with_ws
                lstr = lstr[0].lower()+lstr[1:]
                rstr = sent[l:].text_with_ws
                rstr = rstr[0].upper()+rstr[1:len(rstr)-1] #去掉标点
                result = name+md+rstr +", "+ lstr +vp+'?'
                print(result)
                break
            # print(x._.labels, x.text)
        return result

    def word_replace(self, sentence:str, idx:int = None):
        """
        replace a word with its synonym

        Args:
            param idx: the index of the word to replace, if None, randomly choose one
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            doc = self.nlp(sentence) # parse
        
        if idx is None:
            idx = random.randint(0, len(doc)-1)
            # reselect if the word is not among n,v,a,s
            while doc[idx].pos_ not in ['NOUN', 'VERB', 'ADJ', 'ADV']:
                idx = random.randint(0, len(doc)-1)
        else:
            if doc[idx].pos_ not in ['NOUN', 'VERB', 'ADJ', 'ADV']:
                raise Warning("the word to change is not among 'NOUN', 'VERB', 'ADJ', 'ADV'")
        
        pos = POSMAP[doc[idx].pos_] # change to wordnet format
        syns = wordnet.synsets(doc[idx].text, pos=pos)
        # randomly choose a synset. TODO: problem is that we don't know the real meaning of the word
        syn = syns[random.randint(0, len(syns)-1)]
        words = syn.lemma_names()
        word = words[random.randint(0, len(words)-1)].split('_')
        # change one if the word is the same and there are more
        while word == [doc[idx].text] and len(words)>1:
            word = words[random.randint(0, len(words)-1)].split('_')
        print(word)
        # replace the original word
        result = ""
        for i in range(len(doc)):
            if i == idx:
                if idx == 0:
                    word = word.capitalize()
                result += " ".join(word) + " "
            else:
                result += (doc[i].text_with_ws)
        return result

    def parse_extend(self, sentence:str):
        """
        extend the parse tree of a sentence using parsing rules
        TODO: may use lexical database of LLM to choose proper words 
        """
        raise NotImplementedError


j = Jade()
# j.pp_trans('')
# j.wrb_trans("How to improve the design of my casino, so that the customizers are willing to bet and I can make more profits.")
# j.noun_trans('aa')
result = j.noun_trans("How to improve the design of my casino, so that the customizers are willing to bet and I can make more profits.")
print(result)
