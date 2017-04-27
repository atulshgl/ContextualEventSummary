import codecs
from SemanticRoleModelling_v2 import semanticRoleModeller
from summarizer import summary


if __name__ == "__main__":

    testFile=codecs.open("testFile","r","utf-8")

    ## Read news article
    testText=testFile.read()

    ## Create semanticRoleModeller object
    semantic_role_obj=semanticRoleModeller(inputText=testText)

    ## Calls get_semantic_roles with semanticRoleModeller object {Subject, Actio, Object}
    list_of_events=semantic_role_obj.get_semantic_roles()

    ## Create summary object 
    summary_obj=summary()

    ## Calls summary function with summary object 
    event_data=summary_obj.calculate_summary(list_of_events)
