# Contextual Event Summary Generation

## Versions
The parser uses Python 2.7, NLTK 3.2.2 and Stanford version 3.7.0

## Installation and Usage
  1. Install nltk:
     ```{r, engine='sh', count_lines}
      $ pip install nltk 
     ```
  2. Download nltk_data:
     ```{r, engine='python', count_lines}
      >>> import nltk
      >>> nltk.download()
     ```
  3. The esp_parser.py script uses jar files present in [stanford-postagger-full-2016-10-31](https://nlp.stanford.edu/software/tagger.shtml) and [stanford-parser-full-2016-10-31](https://nlp.stanford.edu/software/lex-parser.shtml).
  4. Make sure to place unzipped [stanford-postagger-full-2016-10-31](https://nlp.stanford.edu/software/tagger.shtml) and [stanford-parser-full-2016-10-31](https://nlp.stanford.edu/software/lex-parser.shtml) folders in the same folder as esp_parser.py script.
  5. Extract stanford-parser-3.7.0-models.jar in the stanford-parser-full-2016-10-31 folder.
  6. To check the completeness of parser intsallation:
     ```{r, engine='sh', count_lines}
      $ python parser_driver.py
     ```
  7. Install Google NLP dependency
     ```{r, engine='sh', count_lines}
      $ pip install --upgrade google-cloud-language
     ```
  8. Set GOOGLE_APPLICATION_CREDENTIALS environment variable
     ```{r, engine='sh', count_lines}
      $ export GOOGLE_APPLICATION_CREDENTIALS=<path_to_google_service_json_file>
     ```
  9. Install Google Cloud SDK (https://cloud.google.com/sdk/downloads)
  10. Authenticate the Google client
      ```{r, engine='sh', count_lines}
       $ gcloud auth application-default login
      ```
  11. Install Watson NLU dependency
      ```{r, engine='sh', count_lines}
       $ pip install --upgrade watson-developer-cloud
      ```
