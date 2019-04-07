"""
LDA模型
"""

import pandas as pd

negfile = '../tmp/meidi_jd_neg_cut.txt'
posfile = '../tmp/meidi_jd_pos_cut.txt'
stoplist = '../data/stoplist.txt'

neg = pd.read_csv(open(negfile,encoding='utf-8'),header=None)
pos = pd.read_csv(open(posfile,encoding='utf-8'),header=None)
stop = pd.read_csv(open(stoplist,encoding='utf-8'),header=None,sep='tipdm',engine='python')
#sep设置分割词
stop = [' ',''] + list(stop[0])                             #Pandas自动过滤了空格符

neg[1] = neg[0].apply(lambda s: s.split(' '))
neg[2] = neg[1].apply(lambda x: [i for i in x if i not in stop])
pos[1] = pos[0].apply(lambda s: s.split(' '))
pos[2] = pos[1].apply(lambda x: [i for i in x if i not in stop])

from gensim import corpora,models

#负面主题分析
neg_dict = corpora.Dictionary(neg[2])           #建立字典
neg_corpus = [neg_dict.doc2bow(i) for i in neg[2]]
neg_lda = models.LdaModel(neg_corpus,num_topics=3,id2word=neg_dict)         #LDA模型训练
for i in range(3):
    neg_lda.print_topic(i)                                                  #输出每个主题

#正面主题分析
pos_dict = corpora.Dictionary(pos[2])           #建立字典
pos_corpus = [pos_dict.doc2bow(i) for i in pos[2]]
pos_lda = models.LdaModel(pos_corpus,num_topics=3,id2word=pos_dict)         #LDA模型训练
for i in range(3):
    pos_lda.print_topic(i)                                                  #输出每个主题