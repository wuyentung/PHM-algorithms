#%%
import pandas as pd
import numpy as np
import scipy as sc
from scipy import stats
import matplotlib.pyplot as plt
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
#%%

def statistical_test(list1, list2, stitle="statistical_test", xlabel="time", ylabel="count", path="", save_fig=False):
    
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
    plt.figure(figsize=(200, 100), dpi=100)
    A, = plt.plot(delta_index, list1, 's-', color='red', label="before", linewidth=20, ms=50)
    B, = plt.plot(delta_index, list2, 's-', color='blue', label="after", linewidth=20, ms=50)

    plt.title(stitle, fontsize=150)
    plt.xlabel(xlabel, fontsize=100, labelpad = 15)
    plt.ylabel(ylabel, fontsize=100, labelpad = 20)
    plt.xticks(fontsize=100)
    plt.yticks(fontsize=100)

    font1 = {'family' : 'Times New Roman',
    'weight' : 'normal',
    'size'   : 100,
    }
    plt.legend(handles=[A,B], prop=font1)
    
    if save_fig:
        plt.savefig("%s折線圖_%s.png" %(path, stitle))
    plt.show()
    
    ## dtw plot
    # path = dtw.warping_path(list1, list2)
    d, paths = dtw.warping_paths(list1, list2)
    best_path = dtw.best_path(paths)
    if save_fig:
        dtwvis.plot_warping(list1, list2, path, filename="%sDTW_%s.png" %(path, stitle))
    else:
        # dtwvis.plot_warping(list1, list2, path)
        dtwvis.plot_warpingpaths(list1, list2, paths, best_path)
    
    return [mean1, mean2], pvalue_mean, [var1, var2], pvalue_var, [skew1, skew2], [kurt1, kurt2], pvalue_ks, correlation, dtw_distance
#%%
## unit test
if __name__ == "__main__":
    list1 = np.random.normal(size=20)
    list2 = np.random.normal(size=20)
    #%%
    statistical_test(list1, list2)
#%%
