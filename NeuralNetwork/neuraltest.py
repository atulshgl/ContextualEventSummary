import numpy as np
from numpy import exp, array, random, dot
from scipy.special import expit
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
from nltk.parse.stanford import StanfordParser
from nltk.tree import Tree
from nltk.tree import ParentedTree
from collections import defaultdict 
import glob, os
from nltk.corpus   import stopwords
import math
import sys
import json
import codecs
from textblob import TextBlob as tb
from collections import defaultdict



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








class NeuralThinker():
    random.seed(1)
    def __init__(self):
        # Seed the random number generator, so it generates the same numbers
        # every time the program runs.

        self.syn0=x0
        self.syn1=x1


    def __init__(self,x0,x1):
        # Seed the random number generator, so it generates the same numbers
        # every time the program runs.

        self.syn0=x0
        self.syn1=x1


    def nonlin(self,x,deriv=False):
        if(deriv==True):
            return x*(1-x)

        return expit(x)

    # The neural network thinks.
    def think(self, input):
       l1=self.nonlin(np.dot(input,self.syn0))
       l2=self.nonlin(np.dot(l1,self.syn1))
       return l2







#TEST EVENTS START





class NeuralTest():

    def __init__(self,top=3):
        self.readmodel()
        self.x0=0
        self.x1=1
        self.readmodel()
        self.syn0=self.x0
        self.syn1=self.x1
        self.neural_network=NeuralThinker(self.syn0,self.syn1)
        self.t_input=[]
        self.t_output=[]
        self.gtags=["p0000000", "pd000000","pe000000","pi000000","pn000000","pp000000","pr000000","pt000000","px000000","vag0000","vaic000","vaif000","vaii000","vaip000","vais000","vam0000","van0000","vap0000","vasi000","vasp000","vmg0000","vmic000","vmif000","vmii000","vmip000","vmis000","vmm0000","vmn0000","vmp0000","vmsi000","vmsp000","vsg0000","vsic000","vsif000","vsii000","vsip000","vsis000","vsm0000","vsn0000","vssf000","vssi000","vssp000","nc00000","nc0n000","nc0p000","nc0s000","np00000","z0","sp000","#"]
        self.gdict={}
        self.idict={}
        self.setdict()
        self.cur_dir=""
        self.infilename="Corpus.txt"
        self.topk=top

        



    def setdict(self):
        ctr=0
        for tag in self.gtags:
            self.gdict[tag]=ctr
            self.idict[ctr]=tag
            ctr += 1

    def readmodel(self):
        fil = open("model-file","r")
        ctr=0
        construct_x0=[]
        construct_x1=[]
        defaultHiddenNodes=int(fil.readline())
        for i in range(250):
            p1s=map(float,fil.readline().split())
            construct_x0.append(p1s)

        p2s=map(float,fil.readline().split())
        construct_x1=p2s

        self.x0=np.array(construct_x0)
        self.x1=np.array(construct_x1)
        #print self.x0,self.x1
        #print self.x0.shape,self.x1.shape




    def getthinking(self,tagshingle,NN):
        #print tagshingle,"<<<<<<<<<<<<<<<<<<<<<<<<<"
        vec=[0]*250
        for pos in range(5):
            #print pos
            if (pos<len(tagshingle)):
                thistag=tagshingle[pos][1]
                if(thistag not in self.gdict):
                    thistag="#"
                #print tagshingle[pos][0],"=",thistag

                vec[pos*50 + self.gdict[thistag]]=1
                #print "Setting: vec[",pos*50 + gdict[thistag],"] = ",1
        vec=array(vec)
        #print len(vec),"============",len(neural_network.synaptic_weights)
        
        return NN.think(vec)

    def test(self):
        self.runparser2(self.neural_network)

    def testtext(self,text):
        return self.runparsetext(text,self.neural_network)

    def personalTest(self):


        jar = self.cur_dir + 'stanford-postagger-full-2016-10-31/stanford-postagger.jar'
        model = self.cur_dir + 'stanford-postagger-full-2016-10-31/models/spanish-distsim.tagger'


        # Path to spanish parser
        stanford_parser_dir = self.cur_dir + 'stanford-parser-full-2016-10-31/'
        esp_model_path = stanford_parser_dir  + "stanford-parser-3.7.0-models/edu/stanford/nlp/models/lexparser/spanishPCFG.ser.gz"
        my_path_to_models_jar  = stanford_parser_dir + "stanford-parser-3.7.0-models.jar"
        my_path_to_jar = stanford_parser_dir  + "stanford-parser.jar"



        in_file =codecs.open(self.infilename, "r", encoding="utf-8")        
        ctr=0
        sentences=[]
        for article in in_file:
            
        
            if(ctr%2==0):
                #print filename,text
                self.runparsetext(article,self.neural_network)
                sentences= article.split('.')
            else:
                print ctr/2
            ctr +=1


    def runparser2(self,NN):


        jar = self.cur_dir + 'stanford-postagger-full-2016-10-31/stanford-postagger.jar'
        model = self.cur_dir + 'stanford-postagger-full-2016-10-31/models/spanish-distsim.tagger'


        # Path to spanish parser
        stanford_parser_dir = self.cur_dir + 'stanford-parser-full-2016-10-31/'
        esp_model_path = stanford_parser_dir  + "stanford-parser-3.7.0-models/edu/stanford/nlp/models/lexparser/spanishPCFG.ser.gz"
        my_path_to_models_jar  = stanford_parser_dir + "stanford-parser-3.7.0-models.jar"
        my_path_to_jar = stanford_parser_dir  + "stanford-parser.jar"



        owd = os.getcwd()
        s=sys.argv
        out_file=codecs.open("out_file", 'w', encoding='utf-8')
        in_file =codecs.open(self.infilename, "r", encoding="utf-8")        
        all_text=[]

        ctr=0
        sentences=[]
        tsentences=[]
        for article in in_file:
            out_file.write('\n')
            
        
            if(ctr%2==0):
                #print filename,text
                sentences= article.split('.')


            else:
                print ctr/2
                #print len(sentences)
                candidates=[]
                for i in range(len(sentences)):
                    sentence = sentences[i]
                    if(sentence!="\n"):
                        print sentence
                        sent = spanishPOSTagger(jar,model)
                        taglist= sent.tag(sentence)
                        shinglesize=5
                        for i in range(len(taglist)):
                            sentence_shingle=taglist[i:i+shinglesize]
                            stripped_shingle=[item[0] for item in sentence_shingle]
                            
                            value=self.getthinking(sentence_shingle,NN)
                            candidates.append((stripped_shingle,value))


                candidates=sorted(candidates, key=lambda x: x[1])

                print "-----------------------------------------"
                for i in range(len(candidates[-self.topk:])):
                    print ' '.join(candidates[i][0])
                print "-----------------------------------------"
            ctr+=1
        out_file.close()

    def runparsetext(self,text,NN):

        jar = self.cur_dir + 'stanford-postagger-full-2016-10-31/stanford-postagger.jar'
        model = self.cur_dir + 'stanford-postagger-full-2016-10-31/models/spanish-distsim.tagger'
        # Path to spanish parser
        stanford_parser_dir = self.cur_dir + 'stanford-parser-full-2016-10-31/'
        esp_model_path = stanford_parser_dir  + "stanford-parser-3.7.0-models/edu/stanford/nlp/models/lexparser/spanishPCFG.ser.gz"
        my_path_to_models_jar  = stanford_parser_dir + "stanford-parser-3.7.0-models.jar"
        my_path_to_jar = stanford_parser_dir  + "stanford-parser.jar"



        
        
        sentences= text.split('.')
        candidates=[]
        for i in range(len(sentences)):
            sentence = sentences[i]
            if(sentence!="\n"):
                print sentence
                sent = spanishPOSTagger(jar,model)
                taglist= sent.tag(sentence)
                shinglesize=5
                for i in range(len(taglist)):
                    sentence_shingle=taglist[i:i+shinglesize]
                    stripped_shingle=[item[0] for item in sentence_shingle]
                    
                    value=self.getthinking(sentence_shingle,NN)
                    candidates.append((stripped_shingle,value))


        candidates=sorted(candidates, key=lambda x: x[1])

        print "-----------------------------------------"
        returnlist=[]
        for i in range(len(candidates[-3:])):
            returnlist.append(' '.join(candidates[i][0]))
            print ' '.join(candidates[i][0])
        print "-----------------------------------------"

        return returnlist
        
        




#TESTEVENTS END

if __name__ == "__main__":

    #Intialise a single neuron neural network.
    test=NeuralTest()
    test.test()


