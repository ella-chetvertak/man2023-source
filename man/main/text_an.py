import re, random, os, codecs, pymorphy3
from operator import itemgetter
from nltk.tokenize import sent_tokenize

morph = pymorphy3.MorphAnalyzer(lang='uk')


class TextAnalyser:
    def __init__(self, data, with_file, group_size, freq):
        self.resultsPop = []
        self.resultsRare = []
        self.resCtx = ''
        self.sortedArr = []
        self.cleanArr = []
        self.ctxLineArr = []
        self.data = data
        self.text = []
        self.withFile = with_file
        self.groupSize = group_size
        self.elemFreq = freq

    def filter_text(self, data):
        wordsArr = []
        self.text = []
        self.ctxLineArr = []
        randkey = random.randint(100000, 999999)
        if self.withFile:
            with open(f"{randkey}.txt", "wb+") as file:
                for chunk in data.chunks():
                    file.write(chunk)
            file = codecs.open(f"{randkey}.txt", "r", "utf-8")
            self.text = file.read().splitlines()
            file.close()
            os.remove(f"{randkey}.txt")
        else:
            split = data.splitlines()
            for elem in split:
                for sent in sent_tokenize(elem):
                    self.text.append(sent)

        for i in range(len(self.text)):
            lst = self.text[i].split(" ")
            wordsArr.append(lst)
            for j in range(len(lst)):
                self.ctxLineArr.append(i)
        # робимо з двухетажного масиву одноетажний
        flatArr = [item for sublist in wordsArr for item in sublist]
        restr = r"[^A-Za-zА-Яа-яіІїЇёЁєЄ0-9\[\]]"
        i = 0
        while i < len(flatArr):
            # фільтрація символів
            isAdded = False
            if '[' in flatArr[i] and ']' in flatArr[i]:
                findex = flatArr[i].index('[')
                sindex = flatArr[i].index(']')
                brakes = flatArr[i][findex:sindex + 1]
                if sindex < findex:
                    flatArr[i] = re.sub(r'[\[\]]', '', flatArr[i])
                else:
                    flatArr[i] = flatArr[i].replace(brakes, '')
                    flatArr.insert(i + 1, brakes)
                    self.ctxLineArr.insert(i + 1, self.ctxLineArr[i])
                    isAdded = True
            elif '[' in flatArr[i] or ']' in flatArr[i]:
                flatArr[i] = re.sub(r'[\[\]]', '', flatArr[i])
            flatArr[i] = flatArr[i].casefold()
            if flatArr[i] != '':
                first = re.findall(restr, flatArr[i][0])
                second = re.findall(restr, flatArr[i][-1])
            else:
                first = ''
                second = ''
            while first and len(flatArr[i]) > 1:
                flatArr[i] = flatArr[i][1:]
                first = re.findall(restr, flatArr[i][0])
            while second and len(flatArr[i]) > 1:
                flatArr[i] = flatArr[i][0:len(flatArr[i]) - 1]
                second = re.findall(restr, flatArr[i][-1])
            if isAdded:
                i += 2
                isAdded = False
            else:
                i += 1
        # сортуємо отриманий масив із чистих слів
        self.cleanArr = flatArr
        self.sortedArr = sorted(flatArr)
        self.sortedArr.append('')

    def at_start(self):
        self.filter_text(self.data)

    def analyse_popular(self):
        word = []

        prevElem = ""
        elemCount = 1

        maxLen = len(max(self.sortedArr, key=len))
        for i in range(3, maxLen + 1):
            word.append({0: 0})
        for elem in self.sortedArr:
            # задаємо довжину слова, також якщо попереднє слово дорівнює нинішньому, прибавляємо лічильник на 1
            length = len(prevElem)
            if prevElem == elem:
                elemCount += 1
            else:
                # йде перевірка на довжину слова
                for i in range(3, maxLen + 1):
                    k = i - 3
                    if length == i:
                        # сортуємо словник по значенню (кількості слів)
                        word[k] = dict(sorted(word[k].items(), key=itemgetter(1)))
                        listValue = list(word[k].values())
                        if min(listValue) < elemCount:
                            # якщо мінімальне з значень словника менше за кількість нового слова, додаємо його у словник та видаляємо мінімальне
                            if len(word[k]) >= self.groupSize:
                                listKeys = list(word[k].keys())
                                word[k].pop(listKeys[listValue.index(min(listValue))])
                            word[k][prevElem] = elemCount
                        break
                elemCount = 1
            prevElem = elem
        resultsPop = '<table><tr><td>Довжина слова</td><td>Слово</td><td>Частотність слова</td></tr>'
        for elem in reversed(word):
            sortEl = dict(sorted(elem.items(), key=itemgetter(1), reverse=True))
            if len(sortEl) != 1:
                for word in sortEl.keys():
                    if sortEl[word] != 0:
                        resultsPop += f'<tr><td>{maxLen}</td><td>{word}</td><td>{sortEl[word]}</td></tr>'
            maxLen -= 1
        resultsPop += '</table>'
        self.resultsPop = resultsPop

    def analyse_rare(self):
        rareWords = []
        prevElem = ""
        elemCount = 1
        for elem in self.sortedArr:
            # задаємо довжину слова, також якщо попереднє слово дорівнює нинішньому, прибавляємо лічильник на 1
            if prevElem == elem:
                elemCount += 1
            else:
                if elemCount == self.elemFreq:
                    rareWords.append(prevElem)
                elemCount = 1
            prevElem = elem

        results = f"Усього слів у тексті з частотою вживання {self.elemFreq}: {len(rareWords)}<br>"
        results += f"Відсоток кількості слів у тексті з частотою вживання {self.elemFreq} до кількості усіх слів: {round(len(rareWords) / len(self.sortedArr)*100, 5)} %<br>"
        results += f"Повний список слів у тексті з частотою вживання {self.elemFreq}:<br><br>"
        
        for element in rareWords:
            res1 = re.findall(r'[A-Za-z\-]', element)
            if len(res1) < len(element) and len(res1) != 0 and list(set(res1)) != ['-']:
                results += element + f"(анг {res1}), "
            else:
                if element != '':
                    results += element + ', '
        self.resultsRare = results

    def search_ctx(self, req, wcase):
        idx = [x[0] for x in enumerate(self.cleanArr) if x[1].casefold() == req.casefold()]
        self.resCtx = ""
        for elem in idx:
            # запис
            try:
                resOne = self.text[self.ctxLineArr[elem]]
            except IndexError:
                resOne = 'На жаль, щось пішло не так'
            if (resOne not in self.resCtx):
                if wcase and req in resOne:
                    self.resCtx += resOne + "<br><br>"
                elif not wcase:
                    self.resCtx += resOne + "<br><br>"
