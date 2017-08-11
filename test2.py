# coding:utf-8
import codecs
import re
import jieba
import logging
from collections import defaultdict
from gensim import corpora, models


# fileter HTML tag and http link
def filter_tags(text):
    pattern1 = re.compile('\<.+\>')
    pattern2 = re.compile('http://[a-zA-Z0-9.?/&=:]*|://[a-zA-Z0-9.?/&=:]*')
    text = re.sub(pattern=pattern1,repl='',string=text)
    text = re.sub(pattern=pattern2, repl='', string=text)
    return text



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
f = codecs.open('answer_info_1000.txt',"r",'UTF-8')
for line in f:
    print(line.split('\001'))
    # title = filter_tags(title)
    # detail = filter_tags(detail)
