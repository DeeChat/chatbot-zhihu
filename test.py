# coding:utf-8
import codecs
import re
import jieba
import logging
from collections import defaultdict
from gensim import corpora, models

stop_list = set('？ 。 ” “ , 《 》 ！ ： ； 啊 哦 额 吧 啦 的 了 " "'.split())

text = '如何高效的健身？'

question = []
for string in text:
    if string not in stop_list:
        question.append(string)
question = ''.join(question)

print(question)
print(jieba.cut(question))