import evaluate as test
import sys
from SemanticRoleLabelling import semanticRoleLabel
from summarizer import summary
from neuraltest import NeuralTest

if __name__ == "__main__":
    ## Take the test corpus as input
    trainingFile = sys.argv[1]
    
    ## Convert the xml file into text
    text = test.readInput(trainingFile)

    ## Extract the list of events from xml text
    test_events = test.extractEvents(text.encode('utf-8'))

    ## Remove xml tags from the test corpus 
    corpusText = test.getTextFromXML(trainingFile)

    ## Get articles from the XML test corpus
    articleList = test.getListFromXML(text.encode('utf-8'))
    
    taggedEvents = test.getEventList(test_events)


    cumTaggedEvents = []
    cumPredictedEvents = []

    ## Create object of neural network test calss
    nnTest=NeuralTest()
    
    ## Create summary object 
    summary_obj=summary()

    
    n = len(articleList)
    tp,tn,pn = 0, 0, 0
    for i in range(n):
        ## Create semanticRoleModeller object
        semantic_role_obj=semanticRoleLabel(inputText=articleList[i])
        

        ## Call neural net event extractor
        '''eventList = nnTest.testtext(articleList[i])'''

        
        ## Calls get_semantic_roles with semanticRoleModeller object {Subject, Actio, Object}
        list_of_events=semantic_role_obj.get_semantic_roles()

        eventList = []
        for e in list_of_events:
            eventList.append(summary_obj.get_event_as_string(e))

        predictedEvents = test.substringSieve(eventList)
        
        cumPredictedEvents += predictedEvents
        cumTaggedEvents += taggedEvents[i]
        
        #print event_data.keys()
        print '****** Article:', i+1 
        f1,vals =  test.f1Score(predictedEvents,taggedEvents[i])
        print 'F1', f1
        tp += vals[0]
        tn += vals[1]
        pn += vals[2]

    print ''
    print '***** Cumulative'
    print  test.getF1Score(tp,tn,pn), '<- F1'

    
    
