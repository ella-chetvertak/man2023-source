import nltk, csv, requests, string, math, pymorphy3
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.data.path.extend(["C:\\front end 13 08\\djangoMAN/nltk_data", "/home/olegchetvertak/man2023-source/nltk_data"])

morph = pymorphy3.MorphAnalyzer(lang='uk')
stopwords = stopwords.words("ukrainian")

SIA = SentimentIntensityAnalyzer('sentiment/vader_lexicon/vader_lexicon.txt')
stop_words = frozenset(stopwords + list(string.punctuation))


class NLTKAnalyse:
    def __init__(self, sentences, min_ton, max_ton):
        self.sentences = sentences
        self.aver_polarity = 0
        self.aver_percent = 0
        self.min = min_ton
        self.max = max_ton

    def get_every_analyse(self):
        total = ''
        all_polarities = []

        for sentence in self.sentences:
            words = word_tokenize(sentence)
            without_stop_words = [word for word in words if word not in stop_words]
            normal_words = []
            for token in without_stop_words:
                p = morph.parse(token)[0]
                normal_words.append(p.normal_form)

            polarity = SIA.polarity_scores(' '.join(normal_words))["compound"] * 100
            if int(self.max) > int(polarity) > int(self.min):
                total += f'{sentence} ({"%.2f" % polarity} %) '
            all_polarities.append(polarity)

        if len(all_polarities) != 0:
            self.aver_polarity = sum(all_polarities)/(len(all_polarities)*100)
        else:
            self.aver_polarity = 0
        self.aver_percent = self.aver_polarity * 100
        return total
