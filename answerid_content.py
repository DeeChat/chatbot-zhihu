# coding:utf-8
import codecs
import logging
import pickle
import re
from preprocess import filter_tags

# fileter HTML tag and http link
# def filter_tags(text):
#     pattern1 = re.compile('\<.+\>')
#     pattern2 = re.compile('http://[a-zA-Z0-9.?/&=:]*|://[a-zA-Z0-9.?/&=:]*')
#     text = re.sub(pattern=pattern1,repl='',string=text)
#     text = re.sub(pattern=pattern2, repl='', string=text)
#     return text


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# loading question_id to answer_id and num_likes dictionaries
question_answer = pickle.load(open('quesid2ansid_numlikes.txt','rb'))
#f = codecs.open('selected_answer_1000.txt',"r",'UTF-8')
f = codecs.open('answers.txt',"r",'UTF-8')

ansid_content = {}

counts = 0
for line in f:
    answer_id, content, question_id = line.split('\001')[:3]
    # if the answer is the top2 answer
    if answer_id in [x[0] for x in question_answer[question_id]]:
        content = filter_tags(content)
        ansid_content[answer_id] = content
    if counts % 1000 == 0:
        logging.info('finished {}'.format(counts))
    counts += 1




answerid_content_file = open('ansid2content.txt','wb')
pickle.dump(ansid_content, answerid_content_file)
answerid_content_file.close()