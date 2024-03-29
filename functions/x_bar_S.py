#%%
import pandas as pd
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import statsmodels
import statsmodels.formula.api as smf
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
    """以 quantile regression 檢查資料點趨勢

    Args:
        x_bar (list): X bar chart 依照移動時窗所取出的值
        s (list): S chart 依照移動時窗所取出的值
        S_ucl (float): S chart 的 UCL
        alpha (float): 顯著水準

    Returns:
        String: 偵測的結果，回傳內容將在 function x_bar_S 中以 if else 判斷為製程或是量測異常
    """
    # quantile regression 使用細節:
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
def draw_control_chart(data_phase2, cl, sigma, ucl, lcl, stitle, sy, sx=False, text_size=100, title_size=150, lable_size=100, tick_size=100, round_to=4, LINE_WIDTH=20, MARKER_SIZE=50):
    # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplot.html#sphx-glr-gallery-subplots-axes-and-figures-subplot-py
    
    ## 圖片顯示數字的小數點位數
    cl = round(cl, round_to)
    ucl = round(ucl, round_to)
    lcl = round(lcl, round_to)
    
    ## linewidth:線條寬度, linestyle: 線條樣式, color:線條顏色, markersize:點大小, fontsize:字大小
    ## 主要折線線段(粗細20)，轉折點以圓點（大小50）表示，顏色黑色
    plt.plot(data_phase2, linestyle='-', marker='o', color='black', markersize=MARKER_SIZE, linewidth=LINE_WIDTH)
    
    ## 管制圖 UCL, LCL，以紅色虛線表示
    plt.axhline((ucl), color='red', linestyle='--', markersize=MARKER_SIZE, linewidth=LINE_WIDTH)
    plt.axhline((lcl), color='red', linestyle='--', markersize=MARKER_SIZE, linewidth=LINE_WIDTH)
    
    ## 管制圖上下一倍、兩倍標準差，以暗紅色虛線表示
    if (cl + sigma) < ucl:
        plt.axhline((cl + sigma), color='darkred', linestyle=':', markersize=MARKER_SIZE, linewidth=LINE_WIDTH)
    if (cl + 2*sigma) < ucl:
        plt.axhline((cl + 2*sigma), color='darkred', linestyle=':', markersize=MARKER_SIZE, linewidth=LINE_WIDTH)
    if (cl - sigma) > lcl:
        plt.axhline((cl - sigma), color='darkred', linestyle=':', markersize=MARKER_SIZE, linewidth=LINE_WIDTH)
    if (cl - 2*sigma) > lcl:
        plt.axhline((cl - 2*sigma), color='darkred', linestyle=':', markersize=MARKER_SIZE, linewidth=LINE_WIDTH)
    
    ## 管制圖 CL，以藍色虛線表示
    plt.axhline(cl, color='blue')
    
    ## x: 文字顯示的 x 軸位置, y: 文字顯示的 y 軸位置, s: 顯示文字內容, c: 文字顏色
    ## 顯示管制圖 UCL, LCL, CL 上的數值
    plt.text(x=-0.05, y=ucl, s=f"UCL={ucl}", fontsize=text_size, c="red")
    plt.text(x=-0.05, y=lcl, s=f"LCL={lcl}", fontsize=text_size, c="red")
    plt.text(x=-0.065, y=cl, s=f"center line={cl}", fontsize=text_size, c="blue")
    
    ## 設定管制圖標題
    plt.title(stitle, fontsize=title_size)
    
    ## 設定管制圖 x 軸文字，因 x bar 子圖不需要所以以 flag 的方式處理
    if sx:
        plt.xlabel(sx, fontsize=lable_size)
    plt.xticks(fontsize=tick_size)
    
    ## 設定管制圖 y 軸文字
    plt.ylabel(sy, fontsize=lable_size)
    plt.yticks(fontsize=tick_size)
    pass
#%%
def mark_anomaly(indice:list, data_phase2:list, window_size:int, color:str, ls="-", m="o"):
    """為每個有異常的資料加註醒目標示

    Args:
        indice (list): 不同段異常資料的起始 index 值
        data_phase2 (list): phase2 資料
        window_size (int): 移動時窗大小
        color (str): 要使用的顏色
        ls (str, optional): 醒目折線定義. Defaults to "-".
        m (str, optional): 資料點以圓點標示. Defaults to "o".
    """
    for anomaly_idx in indice:
        # https://matplotlib.org/stable/gallery/userdemo/annotate_text_arrow.html#sphx-glr-gallery-userdemo-annotate-text-arrow-py
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D.set_marker
        
        ## 以下是把有問題的序列最後一個 subgroup 標註起來的程式碼，留下來供參
        ## alpha: 白色方框的透明度
        # plt.annotate("%s" %x[-1], xy=(x[-1], y[-1]), verticalalignment='top', horizontalalignment="center", fontsize=GLOBAL.TEXT_SIZE, bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.4))
        
        ## 加粗異常資料
        plt.plot(np.arange(anomaly_idx, anomaly_idx+window_size), data_phase2[anomaly_idx:anomaly_idx+window_size], linestyle=ls, marker=m, color=color, markersize=50+10, linewidth=20+10)
    pass
#%%
def grouping_samples(data_list:list, subgroup_size:int):
    ## 將資料依 sample size 區隔，最後一組如果有不滿 sample size 則捨去

    n_subgroups = len(data_list) // subgroup_size ## 一共有多少組 subgroup
    grouped_data_ls = [data_list[i:i+subgroup_size] for i in range(0, n_subgroups*subgroup_size, subgroup_size)]
    
    ## 留下最後一組的程式碼如下，如最後一組小於 sample size，則將把最後一組不足的 sample 以中位數方式補齊
    # if len(data_ls) % sample_size:
    #     last_sample = data_ls[n_groups * sample_size:]
    #     while len(last_sample) < sample_size:
    #         last_sample.append(np.median(last_sample))
    #     grouped_data_ls.append(last_sample)
    #     n_groups += 1
    
    return grouped_data_ls, n_subgroups
#%%
def x_bar_S (phase1_list, phase2_list, subgroup_size=30, manufacturing_anomaly=False, measurment_anomaly=False, window_size=10, alpha=0.05, stitle="x bar with S chart", \
        xlabel="subgroup", ylabel=["subgroup x bar", "subgroup S"], path=""):

    ## 把 phase1, phase2 的資料依照 sample size 分好
    ## data_list: 要根據 subgroup_size 切割的資料, subgroup_size: 幾筆資料視為一組
    grouped_x_phase1, n_subgroups_phase1 = grouping_samples(data_list=phase1_list, subgroup_size=subgroup_size)
    grouped_x_phase2, n_subgroups_phase2 = grouping_samples(data_list=phase2_list, subgroup_size=subgroup_size)

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
    
    ## 移動時窗偵測異常
    manufacturing_indice = []
    measurement_indice = []
    if manufacturing_anomaly or measurment_anomaly:
        for i in range(n_subgroups_phase2-window_size+1): ## 要取最後一組
            ## 將 phase2 資料依照時窗大小切割
            slided_x_bar = x_bar_phase2[i:i+window_size]
            slided_s = s_phase2[i:i+window_size]
            
            ## 判斷時窗區段的資料是否有異常
            ## x_bar (list): X bar chart 依照移動時窗所取出的值, s (list): S chart 依照移動時窗所取出的值, S_ucl (float): S chart 的 UCL, alpha (float): 顯著水準
            warning_str = detecting_sliding_anomaly(x_bar=slided_x_bar, s=slided_s, S_ucl=S_ucl, alpha=alpha)
            
            ## 判斷與紀錄異常資料的 index
            if "anomaly" not in warning_str: continue
            if manufacturing_anomaly and "manufacturing anomaly" in warning_str:
                manufacturing_indice.append(i)
            if measurment_anomaly and "measurement anomaly" in warning_str:
                measurement_indice.append(i)

    
    ## 繪製 x bar S chart
    ## figsize: 圖片大小, dpi:解析度
    plt.figure(figsize=(200, 100), dpi=100)
    
    ## 圖片會分上下兩張子圖繪製，上方是 x bar chart，下方是 S chart
    ## x bar chart
    ## subplot(2, 1, 1): 在圖片 2 列 1 欄的排列中，在編號為 1 的地方繪製子圖
    plt.subplot(2, 1, 1)
    ## data_phase2: phase2 的資料, cl: phase1 的 cl, sigma: phase1 的 sigma, ucl: phase1 的 ucl, lcl: phase1 的 lcl, stitle: 標題文字, sx: x 軸的文字, sy: y 軸文字
    draw_control_chart(data_phase2=x_bar_phase2, cl=Xbar_cl, sigma=Xbar_sigma, ucl=Xbar_ucl, lcl=Xbar_lcl, stitle=f"x bar chart {stitle}", sy=ylabel[0])
    ## indice (list): 不同段異常資料的起始 index 值, window_size (int): 移動時窗大小, color (str): 要使用的顏色
    mark_anomaly(indice=manufacturing_indice, data_phase2=x_bar_phase2, window_size=window_size, color="brown") # 棕色給製程異常
    mark_anomaly(indice=measurement_indice, data_phase2=x_bar_phase2, window_size=window_size, color="purple") # 紫色給量測異常
    
    ## S chart
    plt.subplot(2, 1, 2)
    draw_control_chart(data_phase2=s_phase2, cl=S_cl, sigma=S_sigma, ucl=S_ucl, lcl=S_lcl, stitle=f"S chart {stitle}", sx=xlabel, sy=ylabel[1])
    mark_anomaly(indice=manufacturing_indice, data_phase2=s_phase2, window_size=window_size, color="brown")
    mark_anomaly(indice=measurement_indice, data_phase2=s_phase2, window_size=window_size, color="purple")
    
    plt.savefig(f"{path}{stitle}.png")
        
    return x_bar_phase2, s_phase2, manufacturing_indice, measurement_indice, Xbar_ucl, Xbar_lcl, Xbar_cl, S_ucl
#%%
## unit test
if __name__ == "__main__":
    phase1 = np.random.normal(size=200, loc=0, scale=1)
    phase2 = np.random.normal(size=2000, loc=0, scale=1.1)+np.concatenate(([0]*1000, np.repeat(np.arange(1, 2, 0.1), 20), [0]*800), axis=None)
    #%%
    # stuff = x_bar_S(phase1_ls=phase1, phase2_ls=phase2v2)
    stuff = x_bar_S(phase1_list=phase1, phase2_list=phase2, measurment_anomaly=True, manufacturing_anomaly=True)
    #%%