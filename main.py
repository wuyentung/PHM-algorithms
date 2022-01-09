#%%
import pandas as pd
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt

from functions.chamber2chamber import *
from functions.ewma import *
from functions.hotelling_t2 import *
from functions.statisticalTest import *
from functions.x_bar_S import *
#%%

# USAGE 
mean, t_test, variance, f_test, skewness, kurtosis, KS, correlation, DTW = statistical_test(before_list, after_list, stitle="機 台 特 徵 一 相 關 性 檢 定", xlabel="time", ylabel="count", path="C://graph/")
group1, group2 = chamber2chamber(machines_df, col_groupby, col_value, stitle="機 台 的 比 較", xlabel="全部", ylabel="機 台", path ="C://graph/")
x_bar_phase2, s_phase2, manufacturing_indice, measurement_indice, Xbar_ucl, Xbar_lcl, Xbar_cl, S_ucl = x_bar_S(phase1_list=phase1_list, phase2_list=phase2_list, subgroup_size=30, manufacturing_anomaly=False, measurment_anomaly=False, window_size=10, alpha=0.05, stitle="x bar with S chart", xlabel="subgroup", ylabel=["subgroup x bar", "subgroup S"], path="C://graph/")
ewma_value = ewma(phase1_list, phase2_list, alpha, L, stitle, xlabel, ylabel, path="C://graph/")
t2_value = hotelling_t2(phase1_df, phase2_df, alpha, stitle, xlabel, ylabel, path="C://graph/")
#%%
