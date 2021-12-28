#%%
import pandas as pd
import numpy as np
import scipy as sc
import matplotlib as plt
import statsmodels
import statsmodels.formula.api as smf
import GLOBAL
#%%
## segement data
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
        String: 偵測的結果，回傳內容將在 function x_bar_S 中以 if else 判斷為製程或是量測異常
    """
    # quantile regression:
    # https://www.statsmodels.org/dev/examples/notebooks/generated/quantile_regression.html
    # https://www.statsmodels.org/stable/generated/statsmodels.regression.quantile_regression.QuantReg.fit.html#statsmodels.regression.quantile_regression.QuantReg.fit
    
    ## quantile regression for x bar
    col_name = "subgroup"
    x_bar_df = pd.DataFrame([[i+1, x_bar[i]] for i in range(len(x_bar))], columns=[col_name, "x_bar"])
    QR_x_bar = smf.quantreg("x_bar ~ " + col_name, x_bar_df).fit()
    # X bar 的係數值: QR_x_bar.params[1]
    
    ## 檢查 x bar 的 quantile regression 是否顯著，判斷是否有異常
    if QR_x_bar.pvalues[1] >= alpha:
        return "X bar 沒有趨勢"

    ## quantile regression for s
    s_df = pd.DataFrame([[i+1, s[i]] for i in range(len(x_bar))], columns=[col_name, "s"])
    QR_s = smf.quantreg("s ~ " + col_name, s_df).fit()
    
    ## 檢查 S 的 quantile regression 是否顯著，判斷異常型態
    if QR_s.pvalues[1] >= alpha:
        ## 檢查 S 的中位數是否有超過 S chart 的 UCL
        if np.median(s) >= S_ucl:
            return "type 5; manufacturing anomaly"
        return "type 6; measurement anomaly"
    ## 檢查 S 的斜率方向
    if QR_s.params[1] > 0:
        return "type 1, 2; manufacturing anomaly"
    return "type 3, 4; measurement anomaly"
#%%
def draw_control_chart(data_phase2, cl, sigma, ucl, lcl, anomaly_idx_ls=[], stitle="normalized gap", sy="y", sx="Subgroups", trace=False, save=False, round_to=4, text_size=30, title_size=120, lable_size=100, tick_size=30):
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplot.html#sphx-glr-gallery-subplots-axes-and-figures-subplot-py
    # figsize should be set in upper fuction
    cl = round(cl, round_to)
    ucl = round(ucl, round_to)
    lcl = round(lcl, round_to)
    if trace:
        print("\n%s: " %stitle)
        print("\tUCL = %s" %cl)
        print("\tLCL = %s" %lcl)
        print("\tCL = %s" %ucl)
    # anomaly_idx_ls = [[0, 1], [3, 4]]
    
    plt.plot(data_phase2, linestyle='-', marker='o', color='black')
    plt.axhline((ucl), color='red', linestyle='--')
    plt.axhline((lcl), color='red', linestyle='--')
    if (cl + sigma) < ucl:
        plt.axhline((cl + sigma), color='darkred', linestyle=':')
    if (cl + 2*sigma) < ucl:
        plt.axhline((cl + 2*sigma), color='darkred', linestyle=':')
    if (cl - sigma) > lcl:
        plt.axhline((cl - sigma), color='darkred', linestyle=':')
    if (cl - 2*sigma) > lcl:
        plt.axhline((cl - 2*sigma), color='darkred', linestyle=':')
    plt.axhline(cl, color='blue')
    plt.text(x=-0.05, y=ucl, s="UCL=%s" %ucl, fontsize=text_size, c="r")
    plt.text(x=-0.05, y=lcl, s="LCL=%s" %lcl, fontsize=text_size, c="r")
    plt.text(x=-0.065, y=cl, s="center line=%s" %cl, fontsize=text_size, c="blue")
    if stitle:
        plt.title('%s' %stitle, fontsize=title_size)
    if sx:
        plt.xlabel("%s" %sx, fontsize=lable_size)
    plt.xticks(fontsize=tick_size)
    plt.ylabel("%s" %sy, fontsize=lable_size)
    plt.yticks(fontsize=tick_size)
    if save:
        plt.savefig("%s.png"%stitle)
    pass
#%%
def mark_anomaly(idx_ls:list, data:list, color:str, ls="-", m="o", one_more_node=True):
    """為每個有異常的資料加註醒目標示

    Args:
        idx_ls (list): 不同段異常資料的起始 index 值
        data (list): phase2 資料
        color (str): 要使用的顏色
        ls (str, optional): [description]. Defaults to "-".
        m (str, optional): [description]. Defaults to "o".
        one_more_node (bool, optional): [description]. Defaults to True.
    """
    for anomaly_idx in idx_ls:
        #TODO 為何要 one_more_node?
        if one_more_node:
            last_anomaly_idx = anomaly_idx + [anomaly_idx[-1]+1]
        else:
            last_anomaly_idx = anomaly_idx
        x=last_anomaly_idx
        y=data[last_anomaly_idx[0]:last_anomaly_idx[-1]+1]
        
        # https://matplotlib.org/stable/gallery/userdemo/annotate_text_arrow.html#sphx-glr-gallery-userdemo-annotate-text-arrow-py
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D.set_marker
        ## 以下是把有問題的序列最後一個 subgroup 標註起來的程式碼，留下來供參
        ## alpha: 白色方框的透明度
        # plt.annotate("%s" %x[-1], xy=(x[-1], y[-1]), verticalalignment='top', horizontalalignment="center", fontsize=GLOBAL.TEXT_SIZE, bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.4))
        plt.plot(x, y, linestyle=ls, marker=m, color=color, markersize=GLOBAL.MARKER_SIZE+10, linewidth=GLOBAL.LINE_WIDTH+10)
    pass
def grouping_samples(data_ls:list, subgroup_size:int):
    ## 將資料依 sample size 區隔，最後一組如果有不滿 sample size 則捨去

    n_subgroups = len(data_ls) // subgroup_size ## 一共有多少組 subgroup
    grouped_data_ls = [data_ls[i:i+subgroup_size] for i in range(0, n_subgroups*subgroup_size, subgroup_size)]
    
    ## 留下最後一組的程式碼如下，以下方法將把不足的最後一組以中位數方式補齊
    # if len(data_ls) % sample_size:
    #     last_sample = data_ls[n_groups * sample_size:]
    #     while len(last_sample) < sample_size:
    #         last_sample.append(np.median(last_sample))
    #     grouped_data_ls.append(last_sample)
    #     n_groups += 1
    
    return grouped_data_ls, n_subgroups
#%%
#%%
def x_bar_S (phase1_ls, phase2_ls, subgroup_size=30, measurment_anomaly=False, \
    manufacturing_anomaly=False, window_size=10, alpha=0.05, stitle="x bar with S chart", \
        xlabel="subgroup", ylabel=["subgroup x bar", "subgroup S"], path="", fast=False, save_fig=False):

    ## 把 phase1, phase2 的資料依照 sample size 分好
    grouped_x_phase1, n_subgroups_phase1 = grouping_samples(data_ls=phase1_ls, subgroup_size=subgroup_size)
    grouped_x_phase2, n_subgroups_phase2 = grouping_samples(data_ls=phase2_ls, subgroup_size=subgroup_size)

    ## 設定 x bar S chart 的各種參數
    c4 = C4[subgroup_size]
    
    s_bar = np.mean([np.std(sample, ddof=1) for sample in grouped_x_phase1])
    s_phase2 = [np.std(sample, ddof=1) for sample in grouped_x_phase2]
    
    S_sigma = s_bar*((1 - c4**2)**0.5)/c4
    S_ucl = s_bar + 3*S_sigma
    S_lcl = 0
    S_cl = s_bar
    
    x_bar = [np.mean(sample) for sample in grouped_x_phase1]
    x_bar_phase2 = [np.mean(sample) for sample in grouped_x_phase2]
    x_bar_bar = np.mean(x_bar)
    
    Xbar_sigma = s_bar / (c4 * subgroup_size ** 0.5)
    Xbar_ucl = x_bar_bar + 3*Xbar_sigma
    Xbar_lcl = x_bar_bar - 3*Xbar_sigma
    Xbar_cl = x_bar_bar
    


    ## 
    anomaly_idx_ls = []
    if detect_measurement_anomaly[0]:
        anomaly_idx_ls = detect_anomaly(method="measurement 1", window_size=LENGTH, x_bar_chart=x_bar_chart, s_chart=s_chart, phase2=phase2, alpha=alpha)

    ## don't plot to save time
    if fast:
        return phase2, x_bar_chart, s_chart
    
    ## plot x bar S chart
    plt.figure(figsize=GLOBAL.FIGSIZE)
    
    plt.subplot(2, 1, 1)
    draw_control_chart(data_phase2=x_bar_phase2, cl=Xbar_cl, sigma=Xbar_sigma, ucl=Xbar_ucl, lcl=Xbar_lcl, anomaly_idx_ls=anomaly_idx_ls, stitle="x bar chart %s" %stitle, sy="x bar", sx=False, trace=False, save=False)
    mark_anomaly(idx_ls=anomaly_idx_ls, data=x_bar_phase2, color="brown", ls="-", m="o")
    mark_anomaly(idx_ls=sliding_anomaly_idx_ls, data=x_bar_phase2, color="purple", one_more_node=False)
    
        
    
    plt.subplot(2, 1, 2)
    draw_control_chart(data_phase2=s_phase2, cl=S_cl, sigma=S_sigma, ucl=S_ucl, lcl=S_lcl, anomaly_idx_ls=anomaly_idx_ls, stitle="S chart %s" %stitle, sy="S", trace=False, save=False, title_size=100)
    mark_anomaly(idx_ls=anomaly_idx_ls, data=s_phase2, color="brown", ls="-", m="o")
    mark_anomaly(idx_ls=sliding_anomaly_idx_ls, data=s_phase2, color="purple", one_more_node=False)
    
    if save_fig:
        plt.savefig("%s.png" %stitle)
    # plt.show()
    # print(sliding_anomaly_idx_ls)
    return phase2, x_bar_chart, s_chart