#%%
import pandas as pd
import numpy as np
import scipy as sc
import matplotlib as plt
import statsmodels
import statsmodels.formula.api as smf
#%%
## segement data
SAMPLE_SIZE = 30
LENGTH = 10
#%%
C4 = {
    2 : 0.7979,
    3 : 0.8862, 
    4 : 0.9213,
    5 : 0.9400,
    6 : 0.9515,
    7 : 0.9594,
    8 : 0.9650,
    9 : 0.9693,
    10 : 0.9727,
    15 : 0.9823,
    25 : 0.9896,
    30 : 0.9914,
} ## reference MDS Statistical Process Control p.14, https://r-bar.net/control-chart-constants-tables-explanations/
A3 = {
    2 : 2.659,
    3 : 1.954, 
    4 : 1.628,
    5 : 1.427,
    6 : 1.287,
    7 : 1.182,
    8 : 1.099,
    9 : 1.032,
    10 : 0.975,
    15 : 0.789,
    25 : 0.606,
} ## reference https://web.mit.edu/2.810/www/files/readings/ControlChartConstantsAndFormulae.pdf
#%%
def detecting_sliding_anomaly(x_bar:list, s:list, S_ucl:float, alpha:float):
    """[summary]

    Args:
        x_bar (list): X bar chart 依照移動時窗所取出的值
        s (list): S chart 依照移動時窗所取出的值
        S_ucl (float): S chart 的 UCL
        alpha (float): 顯著水準

    Returns:
        String: 偵測的結果，回傳將在 function XXX 中判斷是否為製程或是量測異常
    """
    # quantile regression:
    # https://www.statsmodels.org/dev/examples/notebooks/generated/quantile_regression.html
    # https://www.statsmodels.org/stable/generated/statsmodels.regression.quantile_regression.QuantReg.fit.html#statsmodels.regression.quantile_regression.QuantReg.fit
    
    ## quantile regression for x bar
    col_name = "subgroup"
    x_bar_df = pd.DataFrame([[i+1, x_bar[i]] for i in range(LENGTH)], columns=[col_name, "x_bar"])
    QR_x_bar = smf.quantreg("x_bar ~ " + col_name, x_bar_df).fit()
    # X bar 的係數值: QR_x_bar.params[1]
    
    ## 檢查 x bar 的 quantile regression 是否顯著
    if QR_x_bar.pvalues[1] >= alpha:
        return "X bar 沒有趨勢"

    ## quantile regression for s
    s_df = pd.DataFrame([[i+1, s[i]] for i in range(LENGTH)], columns=[col_name, "s"])
    QR_s = smf.quantreg("s ~ " + col_name, s_df).fit()
    
    ## 檢查 S 的 quantile regression 是否顯著
    if QR_s.pvalues[1] >= alpha:
        ## 檢查 S 的中位數是否有超過 S chart 的 UCL
        if np.median(s) >= S_ucl:
            return "type 5"
        return "type 6"
    ## 檢查 S 的斜率方向
    if QR_s.params[1] > 0:
        return "type 1, 2"
    return "type 3, 4"
#%%
def x_bar_S (phase1_ls, phase2_ls, subgroup=30, measurment_anomaly=False, \
    manufacturing_anomaly=False, window_size=10, alpha=0.05, stitle="x bar with S chart", \
        xlabel="subgroup", ylabel=["subgroup x bar", "subgroup S"], path=""):
    pass