# coding:utf-8
import jieba
import logging
from gensim import corpora, models
from gensim.models import word2vec
import numpy as np
import numpy.linalg as LA
from itchat.content import *
import itchat
import pickle

from preprocess import setence2vec, most_similar

# def setence2vec(text, w2v_model, tfidf_model, dictionary, word_list):
#     '''
#     Convert any length of string to a vector of fixed dimensions
#     :param text: type of strings
#     :param w2v_model: trained word2vec model
#     :param tfidf_model: trained tfidf model
#     :param dictionary:  pre-loading dictionary
#     :param word_list:  word_list of dictionary
#     :return: a fixed dimension vector, type of ndarray
#     '''
#     words = jieba.cut(text)
#     vec_bow = dictionary.doc2bow(words)
#     vec_tfidf = tfidf_model[vec_bow]
#     setencevec =  np.zeros(256)
#     for word_index, weight in vec_tfidf:
#         try:
#             setencevec += w2v_model[word_list[word_index]] * weight
#         except:
#             continue
#     setencevec = setencevec/LA.norm(setencevec)
#     return setencevec
#
#
# def most_similar(feature_mat, feature):
#     '''
#     find the most similar features' id in feature_mat
#     :param feature_mat: type of mat
#     :param feature: type of mat
#     :return: feature_id
#     '''
#     similarities = feature * feature_mat
#     a = feature
#     simlist = list(np.array(similarities)[0])
#     b = feature_mat[:,simlist.index(max(simlist))]
#     import ipdb
#     ipdb.set_trace(np)
#     return simlist.index(max(simlist))



# loading cofigurations
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

stop_list = set('？ 。 ” “ , 《 》 ！ ： ； 啊 哦 额 吧 啦 的 了 " "'.split())

# loading models
logging.info('loadding models...')
w2v_model = word2vec.Word2Vec.load('wv.model')
tfidf_model = models.TfidfModel.load('tfidf.model')
dictionary = corpora.Dictionary.load('dict')
token2id = dictionary.token2id
word_list = list(token2id.keys())

# load feature_mat
logging.info('loadding feature mat...')
feature_mat = np.load('feature_mat.npy')
# load featurd_id to question_id dictionary
logging.info('loadding feature_id to question_id dictionary...')
featuresid_questionid = pickle.load(open('feaid2quesid.txt', 'rb'))
# load question_id to answer_id dictionary
logging.info('loadding question_id to answer_id dictionary...')
question_answer = pickle.load(open('quesid2ansid_numlikes.txt','rb'))
# load answer_id to content dictionary
logging.info('loadding answer_id to content dictionary...')
answer_content = pickle.load(open('ansid2content.txt','rb'))


# reply to friends, group or public account
@itchat.msg_register([TEXT], isFriendChat=True, isGroupChat=False, isMpChat=True)
def wechat(msg):
    '''
    reply according to different types of messages
    :param msg: msg can be text and picture, for other types of message, reply '爸爸！'
    :return: response to wechat
    '''
    # input a question
    text = msg['Text']
    # remove stop words
    question = []
    for string in text:
        if string not in stop_list:
            question.append(string)
    question = ''.join(question)
    # convert to vector
    features = setence2vec(question, w2v_model, tfidf_model, dictionary, word_list)
    # shape = (1,256)
    features = np.mat(features)
    # find the most similar questions
    feature_id = most_similar(feature_mat, features)
    # find question id
    question_id = featuresid_questionid[feature_id]
    # get the answer id of the most num_likes
    answer_id, num_likes = question_answer[question_id][np.random.randint(0, len(question_answer[question_id]))]
    logging.info(answer_id)
    # get the content
    content = answer_content[answer_id]
    return content




itchat.auto_login(enableCmdQR=True)
itchat.run()