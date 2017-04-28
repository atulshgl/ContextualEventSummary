# -*- coding: utf-8 -*-
import httplib, urllib, base64
import json
from newspaper import Article
import numpy as np
import codecs
import itertools
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict



class summary(object):

    """
    Summarizer for events from news articles in spanish language. Summarizer has the
    following properties:

    Attributes:
        event: A string representing the event captured from semanticRoleLabel
        event_data: A dictionary containing information for each event. Information includes article, raw text, url, summary

    """

    def __init__(self):
        return

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '<subscription-key>',
    }

    def create_params(self,event):

        """ Returns params fed to the bing API"""

        event_dict={'q': event,
            'count': '10',
            'offset': '0',
            'mkt': 'es-es',
            'safeSearch': 'Moderate'}
        params = urllib.urlencode(self.encoded_dict(event_dict))
        return params

    def encoded_dict(self,in_dict):

        """Encodes in UTF-8"""

        out_dict = {}
        for k, v in in_dict.iteritems():
            if isinstance(v, unicode):
                v = v.encode('utf8')
            elif isinstance(v, str):
                # Must be encoded in UTF-8
                v.decode('utf8')
            out_dict[k] = v
        return out_dict


    def calculate_cosine(self,event,headline):

        """Returns cosine similarity values for two TFIDFVectorizers"""

        # Caclulate magnitude of input event
        x = np.array(event)
        mag_event=np.linalg.norm(x)

        # Caclulate magnitude of each sentence from the article
        x = np.array(event)
        mag_headline=np.linalg.norm(x)

        sop=0

        for i in range(len(event)):
            dot_product=event[i]*headline[i]
            sop=sop+dot_product
            tot_mag=float(mag_event*mag_headline)
        return "{:.5f}".format(float(sop)/tot_mag)

    def get_event_as_string(self,event):

        """Returns subject, action, object as event string"""


        final_event_string=""
        if "subject" in event:
            subject=event.get("subject")
            if subject != "NULL":
                final_event_string=subject
        if "action" in event:
            action=event.get("action")
            if action !="NULL":
                final_event_string=final_event_string+" "+action
        if "object" in event:
            event_object=event.get("object")
            if event_object!="NULL":
                final_event_string=final_event_string+" "+event_object

        return final_event_string.strip()


    def calculate_summary(self,list_of_events):

        """ Returns event_data dictionary containing information for each event. 
            Return Format:
            {
             Event1: {article1 :{raw_text:"",url:"",summary:""}, article2:{raw_text:"",url:"",summary:""},... },
             Event2: {article1 :{raw_text:"",url:"",summary:""}, article2:{raw_text:"",url:"",summary:""},... },
             .....
             }

        """

        event_data=defaultdict(lambda:{})
        for event in list_of_events:
            event=self.get_event_as_string(event)
            conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
            params=self.create_params(event)
            conn.request("GET", "/bing/v5.0/news/search?%s" % params, "{body}", self.headers)
            response = conn.getresponse()
            data = response.read()
            j = json.loads(data)
            count=0
            article_data=defaultdict(lambda:{})
            for x in j['value']:
                article = Article(x['url'], language='es')
                article.download()
                article.parse()
                article_text=article.text
                temp=article_text.split('.')
                raw_article=""
                if len(temp)>5:
                    count+=1
                    article_txt=[]
                    article_txt.append(event)
                    for sent in temp:
                        new_sent=sent.replace('\n', "") 
                        raw_article=raw_article+new_sent+". "
                        article_txt.append(new_sent)

                    vect = TfidfVectorizer(min_df=1)
                    tfidf = vect.fit_transform(article_txt)
                    mod_vect=(tfidf * tfidf.T).A
                    input_event=mod_vect[0]
                    cosine_vals={}
                    for i in range(len(mod_vect)-1):
                        article_sentence=mod_vect[i+1]
                        cosine_similarity=self.calculate_cosine(input_event,article_sentence)
                        cosine_vals[i+1]=1.0-float(cosine_similarity)
                    sorted_list= sorted(cosine_vals.items(), key=lambda x: x[1])
                    summary=""

                    top3 = itertools.islice(sorted_list, 3)
                    for summary_sentence in top3:
                        summary_sentence=article_txt[int(summary_sentence[0])]
                        summary=summary+summary_sentence+u". "

                    data={}
                    data["url"]=x['url']
                    data["raw_text"]=raw_article
                    data["summary"]=summary
                    article_data["article"+str(count)]=data

                event_data[event]=article_data
        
        #print event_data
        conn.close()
        return event_data

