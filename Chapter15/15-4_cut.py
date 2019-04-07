"""
分词
"""

import pandas as pd
import jieba

inputfile1 = '../tmp/meidi_jd_neg.txt'
inputfile2 = '../tmp/meidi_jd_pos.txt'
outputfile1 = '../tmp/meidi_jd_neg_cut.txt'
outputfile2 = '../tmp/meidi_jd_pos_cut.txt'

data1 = pd.read_csv(open(inputfile1,encoding='utf-8'),header=None)
data2 = pd.read_csv(open(inputfile2,encoding='utf-8'),header=None)

mycut = lambda x:' '.join(jieba.cut(x))
data1 = data1[0].apply(mycut)
data2 = data2[0].apply(mycut)

data1.to_csv(outputfile1,index=False,header=False,encoding='utf-8')
data2.to_csv(outputfile2,index=False,header=False,encoding='utf-8')