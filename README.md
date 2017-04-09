# Contextual Event Summary Generation

## Versions
The parser uses NLTK 3.2.2 and Stanford version 3.7.0

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
  3. The esp_parser.py script uses jar files present in [stanford-postagger](https://nlp.stanford.edu/software/tagger.shtml) and [stanford-parser](https://nlp.stanford.edu/software/lex-parser.shtml).
  4. Make sure to place unzipped [stanford-postagger](https://nlp.stanford.edu/software/tagger.shtml) and [stanford-parser](https://nlp.stanford.edu/software/lex-parser.shtml) files in the same folder as esp_parser.py script.
  5. Extract stanford-parser-3.7.0-models.jar in the stanford-parser-full-2016-10-31 folder.
