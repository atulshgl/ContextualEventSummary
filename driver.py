# -*- coding: utf-8 -*-  
from esp_parser import spanishPOSTagger,spanishParser
import os

cur_dir = os.path.join(os.path.dirname(__file__))

# Add the jar and model via their path (instead of setting environment variables):
# Path to spanish POS tagger
jar = cur_dir + '/stanford-postagger-full-2016-10-31/stanford-postagger.jar'
model = cur_dir + '/stanford-postagger-full-2016-10-31/models/spanish-distsim.tagger'

# Path to spanish parser
stanford_parser_dir = cur_dir + '/stanford-parser-full-2016-10-31/'
esp_model_path = stanford_parser_dir  + "stanford-parser-3.7.0-models/edu/stanford/nlp/models/lexparser/spanishPCFG.ser.gz"
my_path_to_models_jar  = stanford_parser_dir + "stanford-parser-3.7.0-models.jar"
my_path_to_jar = stanford_parser_dir  + "stanford-parser.jar"

sentence = u'El hardware inalámbrico no autorizado se puede introducir fácilmente.'

sent = spanishPOSTagger(jar,model)
print sent.tag(sentence)


parser = spanishParser(esp_model_path, my_path_to_models_jar, my_path_to_jar)
parser.parse(sentence)
print parser.getPhrase('grup.verb')
