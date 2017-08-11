# coding:utf-8
import codecs
import re
import jieba
import logging
from collections import defaultdict
from gensim import corpora, models

from preprocess import filter_tags

# fileter HTML tag and http link
# def filter_tags(text):
#     pattern1 = re.compile('\<.+\>')
#     pattern2 = re.compile('http://[a-zA-Z0-9.?/&=:]*|://[a-zA-Z0-9.?/&=:]*')
#     text = re.sub(pattern=pattern1,repl='',string=text)
#     text = re.sub(pattern=pattern2, repl='', string=text)
#     return text


def save_model(file):
    # loading cofigurations
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    f = codecs.open(file,"r",'UTF-8')
    stop_list = set('？ 。 ” “ , 《 》 ！ ： ； 啊 哦 额 吧 啦 的 了 " "'.split())
    documents = []
    for line in f:
        words = []
        id, title, detail = line.split('\001')[:3]
        title = filter_tags(title)
        detail = filter_tags(detail)
        title_words = jieba.cut(title)
        detail_words = jieba.cut(detail)
        for word in title_words:
            if word not in stop_list:
                words.append(word)
        for word in detail_words:
            if word not in stop_list:
                words.append(word)
        documents.append(words)
    # build dictionary
    frequency = defaultdict(int)
    for text in documents:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 5] for text in documents]

    dictionary_texts = corpora.Dictionary(texts)
    dictionary_texts.save('dict')
    # build corpus
    corpus = [dictionary_texts.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('corpus', corpus)

    # build model
    tfidf = models.TfidfModel(corpus)
    tfidf.save('tfidf.model')


if __name__ == '__main__':
    save_model('selected_question_1000.txt')

