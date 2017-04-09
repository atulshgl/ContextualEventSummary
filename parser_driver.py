# -*- coding: utf-8 -*-  
from esp_parser import spanishPOSTagger, spanishParser
import os, codecs, time
start_time = time.time()

cur_dir = os.path.join(os.path.dirname(__file__))
input_file = cur_dir + 'article.txt'
output_file = cur_dir + 'phrases.txt'

# Add the jar and model via their path (instead of setting environment variables):
# Path to spanish POS tagger
jar = cur_dir + 'stanford-postagger-full-2016-10-31/stanford-postagger.jar'
model = cur_dir + 'stanford-postagger-full-2016-10-31/models/spanish-distsim.tagger'

# Path to spanish parser
stanford_parser_dir = cur_dir + 'stanford-parser-full-2016-10-31/'
esp_model_path = stanford_parser_dir  + "stanford-parser-3.7.0-models/edu/stanford/nlp/models/lexparser/spanishPCFG.ser.gz"
my_path_to_models_jar  = stanford_parser_dir + "stanford-parser-3.7.0-models.jar"
my_path_to_jar = stanford_parser_dir  + "stanford-parser.jar"

''' Sample sentences in spanish
sentence = u'El hardware inalámbrico no autorizado se puede introducir fácilmente.'
sentence = u'Un equipo de asesores bienintencionado que trabaja en una sala de conferencias podría instalar un punto de acceso inalámbrico para compartir un solo puerto cableado en la sala.'
sentence = u'la India se convirtió en una nación independiente en 1947, tras una lucha por la independencia que estuvo marcada por un movimiento de no violencia.'
sentence = u'Cabe agregar que en aquel tiempo, Malcolm X había sido suspendido de la Nación del Islam debido a unos comentarios inadecuados sobre el asesinato de John F. Kennedy.'
'''

''' Sample code for POS tagging
sent = spanishPOSTagger(jar,model)
print sent.tag(sentence)
'''

''' Sample code for Parsing a sentence
parser = spanishParser(esp_model_path, my_path_to_models_jar, my_path_to_jar)
parse_tree = parser.parse(sentence)
#parser.drawParseTree()
print parser.getPhrase('grup.verb')
'''
def readInput(file_path):
    sentences = []
    with codecs.open(file_path, 'r', 'utf-8') as f:
        paras = f.readlines()
        for para in paras:
            sentences += para.split('.')
    return filter(None, map(unicode.strip, sentences))

def savePhrases(output_file, phrases):
    with codecs.open(output_file,'w', 'utf-8') as f:
        for phrase in phrases:
            f.write(phrase + u'\n')


sentences = readInput(input_file)

parser = spanishParser(esp_model_path, my_path_to_models_jar, my_path_to_jar)

phrases = []
for line in sentences:
    #print 'line:', line
    parser.parse(line)
    phrases += parser.getPhrase('grup.nom')

savePhrases(output_file, set(phrases))

print("--- %s seconds ---" % (time.time() - start_time))
