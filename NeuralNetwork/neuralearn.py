import numpy as np
from numpy import exp, array, random, dot
from scipy.special import expit

# -*- coding: utf-8 -*-  
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
from nltk.parse.stanford import StanfordParser
from nltk.tree import Tree
from nltk.tree import ParentedTree
from collections import defaultdict 
import glob, os
from nltk.corpus   import stopwords
stopSet = set(stopwords.words('spanish'))
import math
import sys
import json
import codecs
from textblob import TextBlob as tb
from collections import defaultdict

#defaultHiddenNodes = 500









class spanishPOSTagger(object):
    """A POS Tagger for spanish language. spanishPOSTagger has the
    following properties:

    Attributes:
        jar: A string representing path to stanford POS tagger jar file.
        model: A string represnting path to spanish tagger file.
        tags: A list of word - POS tuples
    """

    def __init__(self, jar, model,tags = []):
        """Return a spanishPOSTagger object."""
        self.jar = jar
        self.model = model
        self.tags = tags
        stopSet = set(stopwords.words('spanish'))

    def tag(self, sentence):
        """Return a list containing tokenized words and their POS tags."""
        pos_tagger = StanfordPOSTagger(self.model, self.jar, encoding='utf8')
        self.tags = pos_tagger.tag(word_tokenize(sentence))
        return self.tags


class spanishParser(object):
    """A parser for spanish language. spanishParser has the
    following properties:

    Attributes:
        esp_model_path: A string representing path to stanford spanish model file.
        path_to_models_jar: A string represnting path to parser models jar file.
        path_to_jar: A string representing path to stanford parser jar file.
        phrase_list: A list of phrases of the given type.
        parse_tree = A list iterator for the parsed sentence
    """

    def __init__(self, esp_model_path, path_to_models_jar, path_to_jar):
        """Return a spanishParser object."""
        self.esp_model_path = esp_model_path
        self.path_to_models_jar = path_to_models_jar
        self.path_to_jar = path_to_jar
        self.phrase_list = []

    def parse(self, sentence):
        """Set the parse tree property for the given sentence."""
        parser=StanfordParser(model_path=self.esp_model_path, path_to_models_jar=self.path_to_models_jar, path_to_jar=self.path_to_jar, encoding='utf8')
        self.parse_tree = parser.raw_parse(sentence)
        return self.parse_tree

    def getPhrase(self,phrase_type):
        """Return a list of phrases of the given type."""
        parsestr = ''
        for line in self.parse_tree:
            for sentence in line:
                parsestr += str(sentence)
        
        for i in Tree.fromstring(parsestr).subtrees():
            if i.label() == phrase_type:
                self.phrase_list.append(" ".join(str(x) for x in i.leaves()))
        return self.phrase_list

    def drawParseTree(self):
        '''Draw GUI for the parse tree'''
        for line in self.parse_tree:
            for sentence in line:
                sentence.draw()

    def getTree(self):
        return self.parse_tree






class NeuralNetwork():
    random.seed(1)
    def __init__(self):
        self.setrandomweights(500)
        self.syn0=self.x0
        self.syn1=x1

    def __init__(self,dN):
        self.setrandomweights(dN)
        self.syn0=self.x0
        self.syn1=self.x1

    def setrandomweights(self,dN):   
        self.x0 = 2*np.random.random((250,dN)) - 1
        self.x1 = 2*np.random.random((dN,1)) - 1


    def nonlin(self,x,deriv=False):
        if(deriv==True):
            return x*(1-x)

        return expit(x)

         
       
    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations=3000):
        for j in xrange(number_of_training_iterations):
            l0=training_set_inputs
            l1=self.nonlin(np.dot(l0,self.syn0))
            l2=self.nonlin(np.dot(l1,self.syn1))

            l2_error = training_set_outputs-l2

            if(j%1000)==0:
                print "error:"+ str(np.mean(np.abs(l2_error)))

            l2_delta=l2_error*self.nonlin(l2,deriv=True)
            l1_error=l2_delta.dot(self.syn1.T)

            l1_delta=l1_error*self.nonlin(l1,deriv=True)

            self.syn1 += l1.T.dot(l2_delta)
            self.syn0 += l0.T.dot(l1_delta)

        

    # The neural network thinks.
    def think(self, input):
       l1=self.nonlin(np.dot(input,self.syn0))
       l2=self.nonlin(np.dot(l1,self.syn1))
       return l2







class Trainer():

    def __init__(self,dN=500):
        self.cur_dir=""
        self.infilename="Corpus.txt"
        self.defaultHiddenNodes=dN
        self.neural_network = NeuralNetwork(self.defaultHiddenNodes)
        self.training_set_input = array([])
        self.training_set_output = array([])
        self.t_input=[]
        self.t_output=[]
        self.gtags=["p0000000", "pd000000","pe000000","pi000000","pn000000","pp000000","pr000000","pt000000","px000000","vag0000","vaic000","vaif000","vaii000","vaip000","vais000","vam0000","van0000","vap0000","vasi000","vasp000","vmg0000","vmic000","vmif000","vmii000","vmip000","vmis000","vmm0000","vmn0000","vmp0000","vmsi000","vmsp000","vsg0000","vsic000","vsif000","vsii000","vsip000","vsis000","vsm0000","vsn0000","vssf000","vssi000","vssp000","nc00000","nc0n000","nc0p000","nc0s000","np00000","z0","sp000","#"]
        self.gdict={}
        self.idict={}
        self.setdict()


    def setdict(self):
        ctr=0
        for tag in self.gtags:
            self.gdict[tag]=ctr
            self.idict[ctr]=tag
            ctr += 1
        #print len(gdict),ctr

    def htrainer(self,tagshingle,output):
        vec=[0]*250
        for pos in range(5):
            #print pos
            if (pos<len(tagshingle)):
                thistag=tagshingle[pos][1]
                if(thistag in self.gdict):
                    vec[pos*50 + self.gdict[thistag]]=1
        self.t_input.append(vec)
        if(output==1):
            self.t_output.append(1)
        else:
            self.t_output.append(0)

    def trainer(self,tagshingle, output):
        if(len(tagshingle)>5):
            for i in range(len(tagshingle)):
                self.htrainer(tagshingle[i:i+5],output)
        self.htrainer(tagshingle,output)


    def trainmodel(self):

        self.training_set_inputs = array(self.t_input)
        self.training_set_outputs = array([self.t_output]).T
        self.neural_network.train(self.training_set_inputs,self.training_set_outputs)

    def createModel(self):
        self.runparser() #create input
        self.trainmodel()

    def dumpModel(self):
        fil = open("model-file","w")
        fil.write(str(self.defaultHiddenNodes))
        fil.write("\n")
        for x in self.neural_network.syn0:
            for y in x:
                fil.write(str(y)+" ")
            fil.write("\n")
        #fil.write("\n")
        for x in self.neural_network.syn1:
            for y in x:
                fil.write(str(y)+" ")
        fil.write("\n") 
        fil.close()
        print "File Created"


    def runparser(self):


        jar = self.cur_dir + 'stanford-postagger-full-2016-10-31/stanford-postagger.jar'
        model = self.cur_dir + 'stanford-postagger-full-2016-10-31/models/spanish-distsim.tagger'
        # Path to spanish parser
        stanford_parser_dir = self.cur_dir + 'stanford-parser-full-2016-10-31/'
        esp_model_path = stanford_parser_dir  + "stanford-parser-3.7.0-models/edu/stanford/nlp/models/lexparser/spanishPCFG.ser.gz"
        my_path_to_models_jar  = stanford_parser_dir + "stanford-parser-3.7.0-models.jar"
        my_path_to_jar = stanford_parser_dir  + "stanford-parser.jar"

        s=sys.argv
        out_file=codecs.open("out_file", 'w', encoding='utf-8')
        in_file =codecs.open(self.infilename, "r", encoding="utf-8")
        all_text=[]
        ctr=0
        sentences=[]
        tsentences=[]
        for article in in_file:
            if(ctr%2==0):
                sentences= article.split('.')
            else:
                print "Parsing Text:#",ctr/2

                tsentences=article.split('.')
                for i in range(min(len(sentences),len(tsentences))):
                    sentence = sentences[i]
                    tsentence = tsentences[i]
                    
                    eventset=set([])
                    if(sentence!="\n"):
                        sent = spanishPOSTagger(jar,model)
                        taglist= sent.tag(sentence)
                        temp=tsentence
                        #print temp.rstrip('\n'),"======","\n\n"
                        temp=temp.rstrip('\n')
                        while(True):
                            index1=temp.find('<')
                            #print "index1",index1
                            if(index1>=0):
                                index2=temp.find('>')
                                #print "index2",index2
                                if(index2>=0):
                                    eventstring = temp[index1+1:index2]
                                    eventset.add(eventstring)
                                    temp = temp[index2+1:]
                                else:
                                    break
                            else:
                                break
                        eventlist=[]
                        for eventstring in eventset:
                            tagevent=sent.tag(eventstring)
                            eventlist.append(tagevent)

                        eventwordlist=[]
                        for event in eventlist:
                            concater=[item[0] for item in event]
                            eventwordlist.append(concater)

                        for event in eventwordlist:
                            shinglesize=len(event)
                            for i in range(len(taglist)):
                                sentence_shingle=taglist[i:i+shinglesize]
                                stripped_shingle=[item[0] for item in sentence_shingle]
                                if(stripped_shingle==event):

                                        self.trainer(sentence_shingle,1)
                                else:
                                    if(len(set(stripped_shingle).intersection(event))<1):
                                        self.trainer(sentence_shingle,0)
        

            ctr+=1



if __name__ == "__main__":

    defaultHiddenNodes=500
    if len(sys.argv) > 1:       
        defaultHiddenNodes = int(sys.argv[1])

    #NEEDS Corpus.txt in directory can pass hidden layer as argument
    #usage: train=Trainer()
    #or
    #usage: train=Trainer(300) where 300 is number of nodes in hidden layer
    train=Trainer()

    #CREATES model
    train.createModel()
    #train.neural_network.train(training_set_inputs, training_set_outputs, 3000)

    #DUMPS MODEL in model-file
    train.dumpModel()
    

    