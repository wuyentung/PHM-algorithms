import pandas as pd
import numpy as np
import scipy as sc
import matplotlib as plt

from functions.chamber2chamber import chamber2chamber
from functions.ewma import ewma
from functions.hotelling_t2 import hotelling_t2
from functions.statisticalTest import statistical_test
from functions.x_bar_S import x_bar_S


# USAGE 
mean, t_test, variance, f_test, skewness, kurtosis, KS, correlation, DTW = statistical_test(before_list, after_list, stitle="機 台 特 徵 一 相 關 性 檢 定", path="C://graph")
group1, group2 = chamber2chamber(machines_df, stitle="機 台 的 比 較", path ="C://graph")