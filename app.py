from flask import Flask


app = Flask(__name__)

context = "작고 싸고 very very 엄청좋은 빨간색 냉장고 2th!!  하우젠 냉장고"
category = "TEST0001"
itemid = "ID00000001"


@app.route('/')
def hello_world():
    keywordList = []
    keywordList.append(makeKeyword(context))
    keywordList.append('TEST0001')
    keywordList.append('ID00000001')
    print(keywordList)

    return context

# by micky, pentaworks
# 2021-02-02

# simple keywords maker for searching title in shopping-mall
def makeKeyword(tempText):
    from konlpy.tag import Okt
    from collections import OrderedDict
    from itertools import repeat

    okt = Okt()
    unigram = []
    bigram = []
    trigram = []
    tempList = []
    # 어절분리 및 중복제거를 하지만 순서는 유지할 것 python3.X 기준으로 개발 zip(o) izip(x)
    # 분리된 어절에서 필요없는 품사는 분류 및 제거 (형용사, 알파벳, 관형사, 외국어 및 한자등 기호, 명사, 숫자, 미등록어, 동사 기록)
    for word in list(OrderedDict(zip(tempText.split(), repeat(None)))):
        for token in okt.pos(word):
            if token[1] in ['Adjective','Alpha','Determiner','Foreign','Noun','Number','Unknown','Verb']:
                # Number의 경우 후방 연속되는 단어와 띄어쓰기가 없음.
                if token[1] == "Number":
                    tempList.append(token[0])
                else:
                    tempList.append(token[0] + " ")


    # 키워드 생성하기 전체제목 unigram, bigram, trigram 으로 키워드 생서으 숫자가 있을 경우 후방단어와 띄어쓰기 없음
    resultList = []
    resultList.append(tempText)
    resultList.extend(makeUnigram(tempList)) # merge List
    resultList.extend(makeBigram(tempList)) # merge List
    resultList.extend(makeTrigram(tempList)) # merge List

    return resultList

# unigram maker
def makeUnigram(tempList):
    resultList = []
    for word in tempList:
        resultList.append(word.replace(" ","")) #공백제거 후 사용
    return resultList

# bigram maker
def makeBigram(tempList):
    resultList = []
    for i in range(0, len(tempList)-1):
        resultList.append(tempList[i] + tempList[i+1].replace(" ","")) #후방단어만 공백제거 후 사용
    return resultList

# trigram maker
def makeTrigram(tempList):
    resultList = []
    for i in range(0, len(tempList)-2):
        resultList.append(tempList[i] + tempList[i+1] + tempList[i+2].replace(" ","")) #후방단어만 공백제거 후 사용
    return resultList

if __name__ == '__main__':
    app.run()
