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
def marking(x, y, color='brown', ms=12, lw=8, ls="-", m="o"):
    # https://matplotlib.org/stable/gallery/userdemo/annotate_text_arrow.html#sphx-glr-gallery-userdemo-annotate-text-arrow-py
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D.set_marker
    ## alpha: 透明度
    plt.annotate("%s" %x[-1], xy=(x[-1], y[-1]), verticalalignment='top', horizontalalignment="center", fontsize=50, bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.4)
    )
    plt.plot(x, y, linestyle=ls, marker=m, color=color, markersize=ms, linewidth=lw)
    pass
#%%
def mark_anomaly(idx_ls, data, color="brown", ms=12, lw=8, ls="-", m="o", one_more_node=True):
    for anomaly_idx in idx_ls:
        if one_more_node:
            last_anomaly_idx = anomaly_idx + [anomaly_idx[-1]+1]
        else:
            last_anomaly_idx = anomaly_idx
        marking(x=last_anomaly_idx, y=data[last_anomaly_idx[0]:last_anomaly_idx[-1]+1], color=color, ms=ms, lw=lw, ls=ls, m=m)
    pass
#%%
def plot_xbar_with_S(Xbar_ucl, Xbar_cl, Xbar_lcl, Xbar_sigma, S_ucl, S_cl, S_lcl, S_sigma, x_bar_phase2, s_phase2, save=False, stitle="", vert_line=[], anomaly_idx_ls=[], sliding_anomaly_idx_ls=[], measurement3_idx_ls=[]):
    
    plt.figure(figsize=(50, 30))
    
    plt.subplot(2, 1, 1)
    draw_control_chart(data_phase2=x_bar_phase2, cl=Xbar_cl, sigma=Xbar_sigma, ucl=Xbar_ucl, lcl=Xbar_lcl, anomaly_idx_ls=anomaly_idx_ls, stitle="x bar chart %s" %stitle, sy="x bar", sx=False, trace=False, save=False)
    mark_anomaly(idx_ls=anomaly_idx_ls, data=x_bar_phase2, ms=16, lw=12, ls="-", m="o")
    mark_anomaly(idx_ls=sliding_anomaly_idx_ls, data=x_bar_phase2, color="purple", lw=8, ms=16, one_more_node=False)
    for v in measurement3_idx_ls:
        plt.axvline(x=v, color="red", lw=2)
    for v in vert_line:
        plt.axvline(x=v, color="darkblue", lw=2)
    
    plt.subplot(2, 1, 2)
    draw_control_chart(data_phase2=s_phase2, cl=S_cl, sigma=S_sigma, ucl=S_ucl, lcl=S_lcl, anomaly_idx_ls=anomaly_idx_ls, stitle="S chart %s" %stitle, sy="S", trace=False, save=False, title_size=100)
    mark_anomaly(idx_ls=anomaly_idx_ls, data=s_phase2, ms=16, lw=12, ls="-", m="o")
    mark_anomaly(idx_ls=sliding_anomaly_idx_ls, data=s_phase2, color="purple", lw=8, ms=16, one_more_node=False)
    for v in measurement3_idx_ls:
        plt.axvline(x=v, color="red", lw=2)
    for v in vert_line:
        plt.axvline(x=v, color="darkblue", lw=2)
    if save:
        plt.savefig("X bar with S %s.png" %stitle)
    plt.show()
    pass
#%%
def x_bar_S (phase1_ls, phase2_ls, sample_size=30, measurment_anomaly=False, \
    manufacturing_anomaly=False, window_size=10, alpha=0.05, stitle="x bar with S chart", \
        xlabel="subgroup", ylabel=["subgroup x bar", "subgroup S"], path="", fast=False, save_fig=False):
    
    c4 = C4[sample_size]
    x_phase1 = phase1_ls
    x_phase2 = phase2_ls
    s = [np.std(sample, ddof=1) for sample in x_phase1]
    s_phase2 = [np.std(sample, ddof=1) for sample in x_phase2]
    s_bar = np.mean(s)
    
    S_sigma = s_bar*((1 - c4**2)**0.5)/c4
    S_ucl = s_bar + 3*S_sigma
    S_lcl = 0
    S_cl = s_bar
    
    x_bar = [np.mean(sample) for sample in x_phase1]
    x_bar_phase2 = [np.mean(sample) for sample in x_phase2]
    x_bar_bar = np.mean(x_bar)
    
    Xbar_sigma = s_bar / (c4 * sample_size ** 0.5)
    Xbar_ucl = x_bar_bar + 3*Xbar_sigma
    Xbar_lcl = x_bar_bar - 3*Xbar_sigma
    Xbar_cl = x_bar_bar

    ## setting
    stitle = "%s_%s_%s_%s" %(swiitem, mch_id, target_col, alpha)
    df = filt_df(df=df, swiitem=swiitem, mch_id=mch_id, col_name=[target_col, "ADVICEVALUE", "ACTUALVALUE", "GAP"], sort_ref=sort_ref)

    ## data segment
    grouped_x_phase1, n_x_phase1 = grouping_samples(data_ls=df[target_col].to_list())
    grouped_x_phase2, n_x_phase2 = grouping_samples(data_ls=df[target_col].to_list())

    Xbar_ucl, Xbar_cl, Xbar_lcl, Xbar_sigma, S_ucl, S_cl, S_lcl, S_sigma, x_bar_phase2, s_phase2 = set_Xbar_with_S(x_phase1=grouped_x_phase1, x_phase2=grouped_x_phase2)
    
    ## setting phase2 and charts info
    x_bar_chart = Ctrl_chart(ucl=Xbar_ucl, cl=Xbar_cl, lcl=Xbar_lcl, sigma=Xbar_sigma)
    s_chart = Ctrl_chart(ucl=S_ucl, cl=S_cl, lcl=S_lcl, sigma=S_sigma)
    phase2 = Phase2(
        name="%s_%s" % (mch_id, swiitem), 
        sys_time=df.index.tolist(), 
        norm_gap=df["NORM_GAP"].to_list(), 
        subgroup_idx=np.arange(n_x_phase1).tolist(),
        x_bar = x_bar_phase2, 
        s = s_phase2, 
        col_name=["SYS_TIME", "NORM_GAP", "subgroup_idx", "x_bar", "s"]
        )
    phase2.add_feature(feature_name="ADVICE_VALUE", ls=df["ADVICEVALUE"].to_list())
    phase2.add_feature(feature_name="ACTUAL_VALUE", ls=df["ACTUALVALUE"].to_list())
    phase2.add_feature(feature_name="GAP", ls=df["GAP"].to_list())


    ## measurement anomaly detection
    anomaly_idx_ls = []
    if detect_measurement_anomaly[0]:
        anomaly_idx_ls = detect_anomaly(method="measurement 1", window_size=LENGTH, x_bar_chart=x_bar_chart, s_chart=s_chart, phase2=phase2, alpha=alpha)

    sliding_anomaly_idx_ls = []
    if detect_measurement_anomaly[1]:
        sliding_anomaly_idx_ls, sliding_beta1_ls = detect_anomaly(method="measurement 2.5", window_size=LENGTH, x_bar_chart=x_bar_chart, s_chart=s_chart, phase2=phase2, alpha=alpha)
        phase2.add_feature(feature_name="sliding_beta1", ls=sliding_beta1_ls)
        phase2.add_feature(feature_name="is_sliding_anomaly", ls=[idx_ls[-1] for idx_ls in sliding_anomaly_idx_ls], is_anomaly_idx=True)

    measurement3_idx_ls = []
    if detect_measurement_anomaly[2]:
        measurement3_idx_ls = detect_anomaly(method="measurement 3.1", window_size=LENGTH, x_bar_chart=x_bar_chart, s_chart=s_chart, phase2=phase2, alpha=alpha)
    
    ## don't plot to save time
    if fast:
        return phase2, x_bar_chart, s_chart
    
    ## plot x bar S chart
    plt.figure(figsize=GLOBAL.FIGSIZE)
    
    plt.subplot(2, 1, 1)
    draw_control_chart(data_phase2=x_bar_phase2, cl=Xbar_cl, sigma=Xbar_sigma, ucl=Xbar_ucl, lcl=Xbar_lcl, anomaly_idx_ls=anomaly_idx_ls, stitle="x bar chart %s" %stitle, sy="x bar", sx=False, trace=False, save=False)
    mark_anomaly(idx_ls=anomaly_idx_ls, data=x_bar_phase2, ms=16, lw=12, ls="-", m="o")
    mark_anomaly(idx_ls=sliding_anomaly_idx_ls, data=x_bar_phase2, color="purple", lw=8, ms=16, one_more_node=False)
    
        
    
    plt.subplot(2, 1, 2)
    draw_control_chart(data_phase2=s_phase2, cl=S_cl, sigma=S_sigma, ucl=S_ucl, lcl=S_lcl, anomaly_idx_ls=anomaly_idx_ls, stitle="S chart %s" %stitle, sy="S", trace=False, save=False, title_size=100)
    mark_anomaly(idx_ls=anomaly_idx_ls, data=s_phase2, ms=16, lw=12, ls="-", m="o")
    mark_anomaly(idx_ls=sliding_anomaly_idx_ls, data=s_phase2, color="purple", lw=8, ms=16, one_more_node=False)
    
    if save_fig:
        plt.savefig("%s.png" %stitle)
    # plt.show()
    # print(sliding_anomaly_idx_ls)
    return phase2, x_bar_chart, s_chart