# coding:utf-8
import codecs
import re
import jieba
import numpy as np
from gensim.models import word2vec
from gensim import corpora, models
import logging
import numpy.linalg as LA
import pickle


# fileter HTML tag and http link
def filter_tags(text):
    pattern1 = re.compile('\<.+\>')
    pattern2 = re.compile('http://[a-zA-Z0-9.?/&=:]*|://[a-zA-Z0-9.?/&=:]*')
    text = re.sub(pattern=pattern1,repl='',string=text)
    text = re.sub(pattern=pattern2, repl='', string=text)
    return text


def setence2vec(text, w2v_model, tfidf_model, dictionary, word_list):
    '''
    Convert any length of string to a vector of fixed dimensions
    :param text: type of strings
    :param w2v_model: trained word2vec model
    :param tfidf_model: trained tfidf model
    :param dictionary:  pre-loading dictionary
    :param word_list:  word_list of dictionary
    :return: a fixed dimension vector, type of ndarray
    '''
    words = jieba.cut(text)
    vec_bow = dictionary.doc2bow(words)
    vec_tfidf = tfidf_model[vec_bow]
    setencevec =  np.zeros(256)
    for word_index, weight in vec_tfidf:
        try:
            setencevec += w2v_model[word_list[word_index]] * weight
        except:
            continue
    setencevec = setencevec/LA.norm(setencevec)
    return setencevec



def most_similar(feature_mat, feature):
    '''
    find the most similar features' id in feature_mat
    :param feature_mat: type of mat
    :param feature: type of mat
    :return: feature_id
    '''
    similarities = feature * feature_mat       # shape = (1,1000)
    simlist = list(np.array(similarities)[0])
    return simlist.index(max(simlist))



if __name__ == '__main__':
    # loading cofigurations
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    np.seterr(divide='ignore', invalid='ignore')

    # loading models
    # w2v_model = word2vec.Word2Vec.load('ma/wv.model')
    w2v_model = word2vec.Word2Vec.load('wv.model')
    tfidf_model = models.TfidfModel.load('tfidf.model')
    dictionary = corpora.Dictionary.load('dict')
    token2id = dictionary.token2id
    word_list = list(token2id.keys())
    # loading documents
    # f = codecs.open('selected_question_1000.txt',"r",'UTF-8')
    f = codecs.open('questions.txt',"r",'UTF-8')
    # loading question_id to answer_id dictionary
    logging.info('loadding question_id to answer_id dictionary...')
    question_answer = pickle.load(open('quesid2ansid_numlikes.txt','rb'))
    all_question_ids = set(question_answer.keys())

    # mapping featureid to questionid
    featuresid_questionid = {}
    feature_mat = []
    feature_id = 0
    for counts, line in enumerate(f):
        question_id, title, detail = line.split('\001')[:3]
        if question_id in all_question_ids:
            title = filter_tags(title)
            detail = filter_tags(detail)
            question = title + detail
            features = setence2vec(question, w2v_model, tfidf_model,dictionary, word_list)
            featuresid_questionid[feature_id] = question_id
            feature_id += 1
            feature_mat.append(features)

        if counts % 1000 == 0:
            logging.info('finished {}'.format(counts))

    # saving feature mat and featurd_id to question_id dictionariesrm f
    logging.info('start saving feature mat')
    feature_mat = np.mat(feature_mat).T             # shape = (256, 1000)
    np.save('feature_mat.npy', feature_mat)
    feaid_quesid_file = open('feaid2quesid.txt','wb')
    logging.info('start saving feature_id to question_id dictionary')
    pickle.dump(featuresid_questionid, feaid_quesid_file)
    feaid_quesid_file.close()


    # # input a question
    # question = '如何优雅的和女朋友相处?'
    # # convert to vector
    # features = setence2vec(question, w2v_model, tfidf_model, dictionary, word_list)
    # # normalize
    # features = features/LA.norm(features)
    # features = np.mat(features)                 # shape = (1,256)
    # feature_id = most_similar(feature_mat, features)
    # question_id = featuresid_questionid[feature_id]
    # print(question_id)






















