import codecs, re
from operator import itemgetter
from nltk.tokenize import sent_tokenize


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
        if not self.withFile and not data:
            file = codecs.open('textForm.txt', "r", "utf-8")
            self.text = file.read().splitlines()
            file.close()
        elif not self.withFile:
            self.text = sent_tokenize(data)
        else:
            with open("textForm.txt", "wb+") as destination:
                for chunk in data.chunks():
                    destination.write(chunk)
            file = codecs.open('textForm.txt', "r", "utf-8")
            self.text = file.read().splitlines()
            file.close()

        for i in range(len(self.text)):
            lst = self.text[i].split(" ")
            wordsArr.append(lst)
            for j in range(len(lst)):
                self.ctxLineArr.append(i)
        # робимо з двухетажного масиву одноетажний
        flatArr = [item for sublist in wordsArr for item in sublist]
        for i in range(len(flatArr)):
            # фільтрація символів

            index = ""
            flatArr[i] = flatArr[i].casefold()
            if "-" in flatArr[i]:
                index = flatArr[i].index("-")
                if flatArr[i][-1] != "-" and flatArr[i][0] != "-":
                    # перевіряємо за допомогою regexp, чи знаходиться тире між двома буквами
                    reStr = r"/w"
                    prevPosMatch = re.findall(reStr, flatArr[i][index - 1])
                    nextPosMatch = re.findall(reStr, flatArr[i][index + 1])
                    if len(prevPosMatch) != 0 and len(nextPosMatch) != 0:
                        # якщо ні, видаляємо тире
                        flatArr[i] = flatArr[i].replace("-", "")
                    if flatArr[i][index - 1] == ".":
                        # якщо бачимо, що перед тире є скорочення, анігілюємо частину до тире включно
                        flatArr[i] = flatArr[i].replace(flatArr[i][: index + 1], "")
                else:
                    # якщо тире на кінці або у початку слова, просто його видаляємо
                    flatArr[i] = flatArr[i].replace("-", "")
            # очищаємо слова від усього, окрім букв, цифр і тире за допомогою regexp
            flatArr[i] = re.sub(r"[^A-Za-zА-Яа-яіІїЇёЁєЄ\-]", "", flatArr[i])

            # перевірка на англійські символи в не англійському слові

            # таким чином ми дозволяємо бути словам з тире поміж двох букв, наприклад злато-серебро, і одночасно
            # виключаємо випадок із скороченням
        self.cleanArr = flatArr

        # сортуємо отриманий масив із чистих слів
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
        resultsPop = ''
        for elem in reversed(word):
            sortEl = dict(sorted(elem.items(), key=itemgetter(1), reverse=True))

            resultsPop += f'Довжина слова {maxLen}<br>'

            if len(sortEl) == 1 and list(sortEl.values())[0] == 0:
                resultsPop += 'Слів не знайдено<br>'
            else:
                for word in sortEl.keys():
                    if sortEl[word] != 0:
                        resultsPop += f'{word}: {sortEl[word]}<br>'
            resultsPop += '<br>'
            maxLen -= 1
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

        results = ""
        for element in rareWords:
            res1 = re.findall(r'[A-Za-z\-]', element)
            if len(res1) < len(element) and len(res1) != 0 and list(set(res1)) != ['-']:
                results += element + f"(анг {res1}), "
            else:
                if element != '':
                    results += element + ', '
        self.resultsRare = results

    def search_ctx(self, req):
        idx = [x[0] for x in enumerate(self.cleanArr) if x[1] == req]

        self.resCtx = ""
        for elem in idx:
            # запис
            try:
                resOne = self.text[self.ctxLineArr[elem]]
            except IndexError:
                print('Biective ruined')
                resOne = ''
            if resOne not in self.resCtx:
                self.resCtx += resOne + "<br><br>"
