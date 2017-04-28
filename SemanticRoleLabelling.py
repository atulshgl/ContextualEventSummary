import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features
import codecs
import nltk.data
from google.cloud import language

class semanticRoleLabel(object):

    def __init__(self, inputText, googleLanguageClient = None, watsonClient = None, googleLanguageModel = [], watsonLanguageModel = [], semanticRoleList = [], entitySizeLimit = 5, entities= [], keywords = []):
        self.googleLanguageClient = language.Client()
        self.watsonClient =  self.initialize_watson_client()
        self.inputText = inputText
        self.googleLanguageModel = self.googleLanguageClient.document_from_text(self.inputText, language='es', encoding=language.Encoding.UTF8)      
        self.watsonLanguageModel = self.watsonClient.analyze(text = self.inputText, features=[features.Entities(), features.Keywords(), features.SemanticRoles()])
        self.entitySizeLimit = entitySizeLimit
        self.entities = self.extract_entities()
        self.keywords = self.extract_keywords()
        self.semanticRoleList = semanticRoleList

    def initialize_watson_client(self):
        """ Initialise watson language understanding client.
        """
        naturalLanguageUnderstandingClient = NaturalLanguageUnderstandingV1(
        version='2017-02-27',
        username='<username>',
        password='<password>')
        return naturalLanguageUnderstandingClient

    def extract_entities(self) :
         """ Extract entities from google and watson language model.
         """
         entities = []
         googleEntityList = self.googleLanguageModel.analyze_entities()  
         watsonEntityList = self.watsonLanguageModel['entities']

         for entity in googleEntityList.entities[:self.entitySizeLimit]:
            if len(entity.metadata) > 0:
                entities.append({ 'name' : entity.name, 'metadata' : entity.metadata})
     
         for entity in watsonEntityList[:self.entitySizeLimit]: 
             entities.append({ 'name': entity['text'], 'metadata': entity.get('disambiguation', {})}) 

         return entities

    def extract_keywords(self):
        """ Extract keywords from google and watson language model.
        """
        keywords = [] 
        for keyword in self.watsonLanguageModel['keywords'][:self.entitySizeLimit]:   
            keywords.append(keyword['text'])
        return keywords

    def analyze_syntax(self, languageModel):
         """ Extract tokens from google language model.
         """
         analysis = languageModel.annotate_text(include_entities=False, include_sentiment=False)
         return analysis.tokens

    def dependents(self, tokens, head_index):
        """Returns an ordered list of the token indices of the dependents for
        the given head."""
        # Create head->dependency index.
        head_to_deps = {}
        for i, token in enumerate(tokens):
            head = token.edge_index
            if i != head:
                head_to_deps.setdefault(head, []).append(i)
        return head_to_deps.get(head_index, ())

    def phrase_text_for_head(self, tokens, text, head_index):
        """Returns the entire phrase containing the head token
        and its dependents.
        """
        begin, end = self.phrase_extent_for_head(tokens, head_index)
        return text[begin:end]

    def phrase_extent_for_head(self, tokens, head_index):
        """Returns the begin and end offsets for the entire phrase
        containing the head token and its dependents.
        """
        begin = tokens[head_index].text_begin
        end = begin + len(tokens[head_index].text_content)
        for child in self.dependents(tokens, head_index):
            child_begin, child_end = self.phrase_extent_for_head(tokens, child)
            begin = min(begin, child_begin)
            end = max(end, child_end)
        return (begin, end)

    def phrase_text_for_head_with_restrictedchilds(self, tokens, text, parent_subj, restrictedChilds):
        """Returns the entire phrase containing the head token
        and its dependents excluding .
        """
        begin, end = self.phrase_extent_for_head_with_restrictedchilds(tokens, parent_subj, restrictedChilds)
        return text[begin:end]

    def phrase_extent_for_head_with_restrictedchilds(self, tokens, head_index, restrictedChilds):
        """Returns the begin and end offsets for the entire phrase
        containing the head token and its dependents excluding restricted childs and its dependents.
        """
        if type(restrictedChilds) is not list :
              restrictedChilds = [restrictedChilds]

        begin = tokens[head_index].text_begin
        end = begin + len(tokens[head_index].text_content)
        for child in self.dependents(tokens, head_index):
            if child not in restrictedChilds:
                child_begin, child_end = self.phrase_extent_for_head(tokens, child)
                begin = min(begin, child_begin)
                end = max(end, child_end)
        return (begin, end)
     
    def phrase_text_for_rcmod(self, tokens, verb, text):
            parent_subj = tokens[verb].edge_index 
            parent_subj_text = self.phrase_text_for_head_with_restrictedchilds(tokens, text, parent_subj, verb)
            return parent_subj_text

    def find_triples(self, tokens,
                     left_dependency_label= ['NSUBJ', 'NSUBPASS'],
                     head_part_of_speech='VERB',
                     right_dependency_label=['DOBJ','POBJ']):
        """Generator function that searches the given tokens
        with the given part of speech tag, that have dependencies
        with the given labels.  For each such head found, yields a tuple
        (left_dependent, head, right_dependent), where each element of the
        tuple is an index into the tokens array.
        """
        for head, token in enumerate(tokens):
            if token.part_of_speech == head_part_of_speech:
                children = self.dependents(tokens, head)
                left_deps = []
                right_deps = []
                for child in children:
                    child_token = tokens[child]
                    child_dep_label = child_token.edge_label
                    if child_dep_label in left_dependency_label:
                        left_deps.append(child)
                    elif child_dep_label in right_dependency_label:
                        right_deps.append(child)
                for left_dep in left_deps:
                    for right_dep in right_deps:
                        yield (left_dep, head, right_dep)

    def show_triple(self, tokens, text, triple):
        """Prints the given triple (left, head, right).  For left and right,
        the entire phrase headed by each token is shown.  For head, only
        the head token itself is shown.
        """
        nsubj, verb, dobj = triple

        # Extract the text for each element of the triple.
        nsubj_text = self.phrase_text_for_head(tokens, text, nsubj)
        verb_text = tokens[verb].text_content
    
        if tokens[verb].edge_label == 'RCMOD':
            parent_rcmod = self.phrase_text_for_rcmod(tokens,verb,text)
            index = parent_rcmod.find(nsubj_text)
            if index > -1:
               nsubj_text = parent_rcmod
            else:
               nsubj_text = parent_rcmod + nsubj_text 
      
        dobj_text = self.phrase_text_for_head(tokens, text, dobj)
        text = nsubj_text + ' ' +verb_text + ' '+ dobj_text
        #print (text)
        semanticRole = { 'subject': nsubj_text, 'action': verb_text, 'object': dobj_text }
        self.semanticRoleList.append(semanticRole)  

    def correct_token_begin_position(self, tokens, text):
        """token begin position is returned incorrectly by the API. It count accent characters as extra character.
        """
        beginning = 0
        for token in tokens:
            token.text_begin = text.find(token.text_content, beginning) 
            beginning += len(token.text_content)
        return tokens

    def find_in_keywords_and_entities(self, subject, eobject):
        """ Checks if subject or object exists in keywords or entities in any form.
        """
        for keyword in self.keywords:
            if subject.find(keyword) > -1 or eobject.find(keyword) > -1:
                return True

        for entity in self.entities:
            if subject.find(entity['name']) > -1 or eobject.find(entity['name']) > -1:
                return True 

        return False

    def extract_semantic_roles(self):
        """ extract those semantic role which have any keywords or entities in it. 
        """  
        entitySemanticRoleList = []  
        for semanticRole in self.semanticRoleList:
            subject = semanticRole.get('subject', 'NULL')
            eobject = semanticRole.get('object', 'NULL')
            if self.find_in_keywords_and_entities(subject, eobject):
                entitySemanticRoleList.append(semanticRole) 
     
        for role in self.watsonLanguageModel['semantic_roles']:
            subject = 'NULL'
            eobject = 'NULL'
            action = 'NULL'
            predicate = 0
            if 'subject' in role:
                subject = role['subject'].get('text')
                predicate += 1
            if 'object' in role:
                eobject = role['object'].get('text')
                predicate += 1
            if 'action' in role:
                action = role['action'].get('text')
                predicate += 1
            if self.find_in_keywords_and_entities(subject, eobject) and (predicate > 2 or (action !='NULL' and eobject != 'NULL')) :          
                entitySemanticRoleList.append({'subject':subject, 'action':action, 'object': eobject, 'sentence': role['sentence']})

        return entitySemanticRoleList
     
    def get_semantic_roles(self):
        """ returns semantic roles from input text. 
        """ 
        spanishTokenizer = nltk.data.load("tokenizers/punkt/spanish.pickle")
        testData = spanishTokenizer.tokenize(self.inputText)
        for line in testData:
            document = self.googleLanguageClient.document_from_text(line, language='es', encoding=language.Encoding.UTF8)
            tokens = self.correct_token_begin_position(self.analyze_syntax(document), line)
            for triple in self.find_triples(tokens):
                self.show_triple(tokens, line, triple) 
 
        self.semanticRoleList = self.extract_semantic_roles()
        return self.semanticRoleList
                         
#testFile=codecs.open("testFile","r","utf-8")
#testText=testFile.read()
#semantic_role_obj=semanticRoleModeller(inputText=testText)
#a= semantic_role_obj.get_semantic_roles()
#b =1
