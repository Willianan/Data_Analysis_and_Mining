#利用小波分析进行特征分析

from scipy.io import loadmat
import pywt

mat = loadmat('data/leleccum.mat')
signal = mat['leleccum'][0]
coeffs = pywt.wavedec(signal,'bior3.7',level=5)
