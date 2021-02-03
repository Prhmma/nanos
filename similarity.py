from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import json

class similarity:
    """
    similarity class
    inputs:

        products_services: string with one or more words.
        web_text: string of text data from scraped web page.

    methods:

        init(self, products_services, web_text): initialize object of this class with required arguments
        lemmatize_word(word_token): lemmatize words as part of pre-processing (more info: https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html)
        remove_stopwords(text): remove common and ineffective words from our text as part of pre-processing(more info: https://en.wikipedia.org/wiki/Stop_word)
        remove_non_english(word_tokens): remove non-english words as a part of pre-processing to make to app faster.
        pre_processing(): the class method that calls other pre-processing steps in order.
        similarity_detection(): the main function to calculate the similarity between to given list of words

    """
    def __init__(self, products_services, web_text) -> None:
        nltk.download("wordnet")
        nltk.download("words")
        self.words = set(nltk.corpus.words.words())
        self.lemmatizer = WordNetLemmatizer()
        self.tokenizer = RegexpTokenizer(r"\w+")
        self.products_services = products_services
        self.results = {}
        self.web_text = BeautifulSoup(web_text,'html.parser').text
        self.cleared_text = ""

    def lemmatize_word(self, word_tokens) -> list:
        """
        input:
            list of word tokens
        output:
            list of lemmatized words
        """
        lemmas = [self.lemmatizer.lemmatize(word, pos="v") for word in word_tokens]
        return lemmas

    def remove_stopwords(self, text) -> list:
        """
        input:
            web page text as string
        output:
            list of filtered words 
        """
        text = text.lower()
        stop_words = set(stopwords.words("english"))
        word_tokens = self.tokenizer.tokenize(text)
        filtered_text = [word for word in word_tokens if word not in stop_words]
        return filtered_text

    def remove_non_english(self, word_tokens) -> list:
        """
        input:
            list of word tokens
        output:
            list of filtered words
        """
        return [w for w in word_tokens if w.lower() in self.words or not w.isalpha()]

    def pre_processing(self):
        """
        process products_services and make set of unique words
        then take care of web text with defined pre-processing methods
        """
        self.products_services = self.products_services.lower()
        self.products_services = self.products_services.replace(",", " ")
        self.products_services = re.sub("  +", " ", self.products_services)
        self.products_services = list(set(self.products_services.split()))

        self.cleared_text = re.sub('\d+','',self.web_text)
        self.cleared_text = self.remove_stopwords( self.cleared_text)
        self.cleared_text = self.remove_non_english(self.cleared_text)
        self.cleared_text = self.lemmatize_word(self.cleared_text)
        self.cleared_text = list(set(self.cleared_text))

    def similarity_detection(self,json_output=True) -> dict:
        """
        use WUP similarity score to sort similarity between two given list of words
        input:
            json_output: flag to work with web and cli properly(cli use dict and web app use json)
        output:
            json or dict
        """
        for ps in self.products_services:
            try:
                ps_word = wordnet.synsets(ps)[0]
            except Exception as ex:
                continue
            for word in self.cleared_text:
                try:
                    similarity = ps_word.wup_similarity(wordnet.synsets(word)[0])
                    if similarity != None:
                        if word not in self.results or self.results[word] < similarity:
                            self.results[word] = similarity
                except Exception as ex:
                    pass
        if json_output:
            return json.dumps(json.dumps(sorted(self.results.items(), key=lambda kv: kv[1]))).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
        else:
            return sorted(self.results.items(), key=lambda kv: kv[1])