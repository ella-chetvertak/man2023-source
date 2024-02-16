import nltk, string, pymorphy3
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import codecs, random, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
nltk.data.path.extend([str(BASE_DIR) + "/nltk_data", "/home/olegchetvertak/man2023-source/nltk_data"])

morph = pymorphy3.MorphAnalyzer(lang='uk')
stopwords = stopwords.words("ukrainian")

SIA = SentimentIntensityAnalyzer('sentiment/vader_lexicon/vader_lexicon.txt')
stop_words = frozenset(stopwords + list(string.punctuation))


class NLTKAnalyse:
    def __init__(self, data, with_file, min_ton, max_ton, randkey):
        self.sentences = []
        self.aver_polarity = 0
        self.aver_percent = 0
        self.min = min_ton
        self.max = max_ton
        self.withFile = with_file
        self.data = data
        self.randkey = randkey

    def filter_text(self):
        randkey = None
        if self.withFile or self.randkey:
            if self.withFile:
                with open("keycounter.txt", "r") as keycounter:
                    prevkey = int(keycounter.read())
                    randkey = prevkey + 1
                with open("keycounter.txt", "w") as keycounter:
                    keycounter.write(f"{randkey}")
                with open(f"{randkey}.txt", "wb+") as file:
                    for chunk in self.data.chunks():
                        file.write(chunk)
                file = codecs.open(f"{randkey}.txt", "r", "utf-8")
            elif self.randkey:
                file = codecs.open(f"{self.randkey}.txt", "r", "utf-8")
            parts = file.read().splitlines()
            for elem in parts:
                self.sentences.extend(sent_tokenize(elem))
            file.close()
        else:
            self.sentences = sent_tokenize(self.data)
        return randkey

    def at_start(self):
        return self.filter_text()

    def get_every_analyse(self):
        totalY = [0 for _ in range(-100, 101, 10)]
        totalX = [f'{i} %' for i in range(-100, 101, 10)]
        all_polarities = []
        total = "<table><tr><td>Частина тексту</td><td>Тональність, %</td></tr>"
        for sentence in self.sentences:
            words = word_tokenize(sentence)
            without_stop_words = [word for word in words if word not in stop_words]
            normal_words = []
            for token in without_stop_words:
                p = morph.parse(token)[0]
                normal_words.append(p.normal_form)

            polarity = round(SIA.polarity_scores(' '.join(normal_words))["compound"]*10)*10
            totalY[totalX.index(f'{polarity} %')] += 1
            if int(self.max) >= int(polarity) >= int(self.min):
                total += f"<tr><td>{sentence}</td><td>{polarity}</td></tr>"
            all_polarities.append(polarity)
        total += "</table>"

        if len(all_polarities) != 0:
            self.aver_polarity = sum(all_polarities)/(len(all_polarities)*100)
        else:
            self.aver_polarity = 0
        self.aver_percent = self.aver_polarity * 100
        return totalX, totalY, total
