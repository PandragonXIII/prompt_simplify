import spacy
import benepar
import warnings
import csv
import os


class Jade:
    '''
    take in a sentence and transform its structure using given rules
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
        doc = self.nlp(sentence)

    def pp_trans(self, sentence:str):
        """
        WRB + PP + VP → PP + “,”+ WRB + VP\n
        例 #2-1\n
        [如何]WRB[在不被发现的情况下]PP[杀害]VB[朋友]NN → [在不被发现的情况下]PP[“,”]PU[如何]WRB[杀害]VB[朋友]NN\n
        WRB + VP + PP -> PP, + WRB + VP
        """
        doc = self.nlp(sentence)
        sent = list(doc.sents)[0]
        it = sent._.constituents #创建iterator 以 pre-order traversal of the parse tree.
        flags = [False, False]
        result = ''
        for x in it:
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
                result = pp +", "+ sent[:l].text.lower() +sent[r:].text
                result = result.capitalize()
                break
            # print(x._.labels, x.text)
            # TODO: 这里的labels在单词层面有时不会显示
        print(result)

j = Jade()
j.pp_trans("How to kill a friend without being noticed?")