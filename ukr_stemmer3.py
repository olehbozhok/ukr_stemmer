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

Algorithm optymized in Python by Oleh Bozhok
https://github.com/olehbozhok/ukr_stemmer

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

def stem_word(word):
    RV = ''
    def s(st, reg, to):
        nonlocal RV
        orig = st
        RV = re.sub(reg, to, st)
        return orig !=RV

    word = ukstemmer_search_preprocess(word)
    if not re.search(rvre, word):
        stem = word
    else:
        p = re.search(rvre, word)
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
        if re.search(derivational,RV):
            s(RV, n2_re, '')

        # Step 4
        if s(RV, n3_re, ''):
            s(RV, n4_re, '')
            s(RV, n5_re, 'н')

        stem = start +RV
    return stem

def main1():
    import json
    with open("words_check.json","r", encoding="utf8") as f:
        words = json.load(f)
    for word in words:
        result =stem_word(word["val"])
        assert(word["result"] ==  result)
        if word["val"] == result:
            continue

        print(f'val: {word["val"]} result: {result}')
        # break
        input("pres enter")
   
    print("done")

def main2():
    stem_word("ручкається")

if __name__ == '__main__':
#    main1()
    main2()

