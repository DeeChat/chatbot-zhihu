# coding:utf-8
import codecs
import logging
import pickle
import pprint

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
f = codecs.open('answer_info_1000.txt',"r",'UTF-8')
# f = codecs.open('/home/nfs-deecamp-chatbot/zhihu/data-zhihu/answer_infos.txt',"r",'UTF-8')
question_answer = {}

# save the answer of the top2 num_likes

for line in f:
    answer_id, question_id, num_likes = line.split('\001')[:3]
    num_likes = int(num_likes)
    question_answer[question_id] = question_answer.get(question_id,[]) + [(answer_id, num_likes)]

for key, values in question_answer.items():
    question_answer[key] = sorted(values, key = lambda x:x[1], reverse = True)[:2]


question_answer_file = open('quesid2ansid_numlikes.txt','wb')
pickle.dump(question_answer, question_answer_file)
question_answer_file.close()


