#%%
import pandas as pd
import numpy as np
import scipy as sc
from scipy import stats
import matplotlib.pyplot as plt
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
#%%

def statistical_test(list1, list2, stitle="statistical_test", xlabel="time", ylabel="count", path=""):
    
    if len(list1) != len(list2):
        ValueError("length of list1 and list2 should be the same")
        
    ## t test
    mean1 = np.mean(list1)
    mean2 = np.mean(list2)
    t_score, pvalue_mean = stats.ttest_ind(list1, list2)
    
    ## f test
    var1 = np.var(list1)
    var2 = np.var(list2)
    f_score = np.var(list1, ddof=1)/np.var(list2, ddof=1) #calculate F test statistic 
    dfn = len(list1)-1 #define degrees of freedom numerator 
    dfd = len(list2)-1 #define degrees of freedom denominator 
    pvalue_var = 1 - stats.f.cdf(f_score, dfn, dfd) #find p-value of F test statistic 
    
    ## skewness
    skew1 = stats.skew(list1)
    skew2 = stats.skew(list2)
    
    ## kurtosis
    kurt1 = stats.kurtosis(list1)
    kurt2 = stats.kurtosis(list2)
    
    ## KS test
    ks_score, pvalue_ks = stats.kstest(list1, list2)
    
    ## correlation
    correlation, p_value_corr = stats.pearsonr(list1, list2)
    
    ## dtw distance
    dtw_distance = dtw.distance(list1, list2)
    
    ## 折線圖
    delta_index = np.arange(len(list1)) + 1
    ## figsize:圖片大小, dpi:解析度, linewidth:線條寬度, linestyle: 線條樣式, color:線條顏色, markersize:點大小, fontsize:字大小, label: 線段標示, labelpad: 標籤和該軸之間的間距
    plt.figure(figsize=(200, 100), dpi=100)
    A, = plt.plot(delta_index, list1, 's-', color='red', label="before", linewidth=20, markersize=50)
    B, = plt.plot(delta_index, list2, 's-', color='blue', label="after", linewidth=20, markersize=50)

    plt.title(stitle, fontsize=150)
    plt.xlabel(xlabel, fontsize=100, labelpad = 15)
    plt.ylabel(ylabel, fontsize=100, labelpad = 20)
    plt.xticks(fontsize=100)
    plt.yticks(fontsize=100)

    font1 = {'family' : 'Times New Roman',
    'weight' : 'normal',
    'size'   : 100,
    }
    ## handles: 圖例所使用的線段, prop: 字型、字體設定
    plt.legend(handles=[A,B], prop=font1)
    
    plt.savefig(f"{path}折線圖_{stitle}.png")
    plt.show()
    
    ## dtw plot
    d, paths = dtw.warping_paths(list1, list2)
    best_path = dtw.best_path(paths)
    ## filename: 存檔的名稱
    dtwvis.plot_warpingpaths(list1, list2, paths, best_path, filename=f"{path}DTW_{stitle}.png")
    
    return [mean1, mean2], pvalue_mean, [var1, var2], pvalue_var, [skew1, skew2], [kurt1, kurt2], pvalue_ks, correlation, dtw_distance
#%%
## unit test
if __name__ == "__main__":
    list1 = np.random.normal(size=20)
    list2 = np.random.normal(size=20)
    #%%
    statistical_test(list1, list2)
#%%
