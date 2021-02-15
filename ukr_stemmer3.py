#!/usr/bin/python3

"""
Russian stemming algorithm provided by Dr Martin Porter (snowball.tartarus.org):
http://snowball.tartarus.org/algorithms/russian/stemmer.html

Algorithm implementation in PHP provided by Dmitry Koterov (dklab.ru):
http://forum.dklab.ru/php/advises/HeuristicWithoutTheDictionaryExtractionOfARootFromRussianWord.html

Algorithm implementation adopted for Drupal by Algenon (4algenon@gmail.com):
https://drupal.org/project/ukstemmer

Algorithm implementation in Python by Zakharov Kyrylo
https://github.com/Amice13

"""


import re

vowel = re.compile('аеиоуюяіїє')  # http://uk.wikipedia.org/wiki/Голосний_звук
perfectiveground = re.compile('(ив|ивши|ившись|ыв|ывши|ывшись((?<=[ая])(в|вши|вшись)))$')
 # http://uk.wikipedia.org/wiki/Рефлексивне_дієслово
reflexive = re.compile('(с[яьи])$')
# http://uk.wikipedia.org/wiki/Прикметник + http://wapedia.mobi/uk/Прикметник
adjective = re.compile('(ими|ій|ий|а|е|ова|ове|ів|є|їй|єє|еє|я|ім|ем|им|ім|их|іх|ою|йми|іми|у|ю|ого|ому|ої)$')
# http://uk.wikipedia.org/wiki/Дієприкметник
participle = re.compile('(ий|ого|ому|им|ім|а|ій|у|ою|ій|і|их|йми|их)$')
# http://uk.wikipedia.org/wiki/Дієслово
verb = re.compile('(сь|ся|ив|ать|ять|у|ю|ав|али|учи|ячи|вши|ши|е|ме|ати|яти|є)$')
# http://uk.wikipedia.org/wiki/Іменник
noun = re.compile('(а|ев|ов|е|ями|ами|еи|и|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я|і|ові|ї|ею|єю|ою|є|еві|ем|єм|ів|їв|ю)$')
rvre = re.compile('[аеиоуюяіїє]')
derivational = re.compile('[^аеиоуюяіїє][аеиоуюяіїє]+[^аеиоуюяіїє]+[аеиоуюяіїє].*(?<=о)сть?$')

n1_re = re.compile('и$')
n2_re = re.compile('ость$')
n3_re = re.compile('ь$')
n4_re = re.compile('ейше?$')
n5_re = re.compile('нн$')


def ukstemmer_search_preprocess(word):
    word = word.lower()
    word = word.replace("'", "")
    word = word.replace("ё", "е")
    word = word.replace("ъ", "ї")
    return word

class UkrainianStemmer():
    def __init__(self, word):
        self.word = word
        self.RV = ''

    def s(self, st, reg, to):
        orig = st
        self.RV = reg.sub(to, st)
        return (orig != self.RV)

    def stem_word(self):
        word = ukstemmer_search_preprocess(self.word)
        if not rvre.search(word):
            stem = word
        else:
            p = rvre.search(word)
            start = word[0:p.span()[1]]
            self.RV = word[p.span()[1]:]

            # Step 1
            if not self.s(self.RV, perfectiveground, ''):

                self.s(self.RV, reflexive, '')
                if self.s(self.RV, adjective, ''):
                    self.s(self.RV, participle, '')
                else:
                    if not self.s(self.RV, verb, ''):
                        self.s(self.RV, noun, '')
            # Step 2
            self.s(self.RV, n1_re, '')

            # Step 3
            if re.search(derivational, self.RV):
                self.s(self.RV, n2_re, '')

            # Step 4
            if self.s(self.RV, n3_re, ''):
                self.s(self.RV, n4_re, '')
                self.s(self.RV, n5_re, u'н')

            stem = start + self.RV
        return stem

def stem_word(word):
    RV = ""
    def s(st, reg, to):
        # global RV
        orig = st
        RV = reg.sub(to, st)
        return (orig != RV)

    word = ukstemmer_search_preprocess(word)
    if not rvre.search(word):
        stem = word
    else:
        p = rvre.search(word)
        start = word[0:p.span()[1]]
        RV = word[p.span()[1]:]

        # Step 1
        if not s(RV, perfectiveground, ''):

            s(RV, reflexive, '')
            if s(RV, adjective, ''):
                s(RV, participle, '')
            else:
                if not s(RV, verb, ''):
                    s(RV, noun, '')
        # Step 2
        s(RV, n1_re, '')

        # Step 3
        if re.search(derivational, RV):
            s(RV, n2_re, '')

        # Step 4
        if s(RV, n3_re, ''):
            s(RV, n4_re, '')
            s(RV, n5_re, u'н')

        stem = start + RV
    return stem

if __name__ == '__main__':
    import json
    with open("words_check.json","r", encoding="utf8") as f:
        words = json.load(f)
    results = []
    for word in words:
        stemObj = UkrainianStemmer(word["val"])
        assert(word["result"] == stemObj.stem_word())
        assert(word["result"] == stem_word(word["result"]) )
   
    print("done")

