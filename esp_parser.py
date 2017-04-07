# -*- coding: utf-8 -*-  
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
from nltk.parse.stanford import StanfordParser
from nltk.tree import Tree


class spanishPOSTagger(object):
    """A POS Tagger for spanish language. spanishPOSTagger has the
    following properties:

    Attributes:
        jar: A string representing path to stanford POS tagger jar file.
        model: A string represnting path to spanish tagger file.
        tags: A list of word - POS tuples
    """

    def __init__(self, jar, model,tags = []):
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
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
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.esp_model_path = esp_model_path
        self.path_to_models_jar = path_to_models_jar
        self.path_to_jar = path_to_jar
        self.phrase_list = []

    def parse(self, sentence):
        """Set the parse tree property for the given sentence."""
        parser=StanfordParser(model_path=self.esp_model_path, path_to_models_jar=self.path_to_models_jar, path_to_jar=self.path_to_jar, encoding='utf8')
        self.parse_tree = parser.raw_parse(sentence)

    def getPhrase(self,phrase_type):
        """Return a list of phrases of the given type."""
        parsestr = ''
        for line in list(self.parse_tree):
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
