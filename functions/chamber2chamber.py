#%%
import pandas as pd
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
#%%
def detect_outlier(data_1:pd.Series, threshold:float):
    outliers={}
    
    mean_1 = np.mean(data_1)
    std_1 =np.std(data_1)
    
    for id in data_1.index:
        z_score = (data_1[id] - mean_1)/std_1 
        if np.abs(z_score) > threshold:
            outliers[id] = data_1[id]
    return outliers
#%%
def chamber2chamber(df:pd.DataFrame, col_groupby:str, col_value:str, stitle="chamber", xlabel="all", ylabel="machine", path="", ):
    
    sta_method="std"
    if "mean" == sta_method:
        values = df.groupby(by=col_groupby).mean()[col_value]
    elif "median" == sta_method:
        values = df.groupby(by=col_groupby).median()[col_value]
    elif "var" == sta_method:
        values = df.groupby(by=col_groupby).var()[col_value]
    elif "std" == sta_method:
        values = df.groupby(by=col_groupby).std()[col_value]
    
    ## threshold: 超過平均值多少標準差視為離群資料
    group1 = detect_outlier(values, threshold=2)
    group2 = detect_outlier(values, threshold=3)
    for key2 in group2.keys():
        group1.pop(key2)
    group1_df = pd.DataFrame.from_dict(group1, orient='index', columns=[col_value])
    group2_df = pd.DataFrame.from_dict(group2, orient='index', columns=[col_value])
    
    ## figsize:圖片大小, dpi:解析度, linewidth:線條寬度, linestyle: 線條樣式, color:線條顏色, markersize:點大小, fontsize:字大小, label: 線段標示,
    plt.figure(figsize=(200, 100), dpi=100)
    # https://matplotlib.org/stable/gallery/statistics/boxplot.html
    plt.boxplot(
        values, showmeans=True, meanline=True, 
        boxprops=dict(linewidth=20), 
        medianprops=dict(linewidth=20), 
        whiskerprops=dict(linewidth=20), 
        capprops=dict(linewidth=20), 
        meanprops=dict(linewidth=20, linestyle='--', color="purple"), 
        flierprops=dict(markersize=50, marker='o', markerfacecolor='black'), 
        )
    
    plt.title("%s" %stitle, fontsize=150)
    plt.xlabel("%s" %xlabel, fontsize=100)
    plt.ylabel("%s" %ylabel, fontsize=100)
    plt.xticks(fontsize=100)
    plt.yticks(fontsize=100)
    for key2, value2 in group2.items():
        ## x: 文字顯示的 x 軸位置, y: 文字顯示的 y 軸位置, s: 顯示文字內容, c: 文字顏色
        plt.text(x=1.08, y=value2, s=key2, fontsize=100, color="red")
    for key1, value1 in group1.items():
        plt.text(x=1.08, y=value1, s=key1, fontsize=100, color="blue")
    plt.tight_layout()
    plt.savefig("%s%s.png" %(path, stitle))
    plt.show()
    return group1_df, group2_df
#%%
## unit test
if __name__ == "__main__":
    mchs = {
        "001": np.random.normal(size=20),
        "002": np.random.normal(size=10, loc=.1, scale=.3),
        "003": np.random.normal(size=15, loc=.1, scale=1.2),
        "004": np.random.normal(size=30, loc=.1, scale=10),
        "005": np.random.normal(size=20, loc=.1, scale=1),
        "006": np.random.normal(size=20, loc=.1, scale=100),
    }
    mchs_df = pd.concat([
        pd.DataFrame(mchs["001"], index=["001"]*mchs["001"].size, columns=["value"]), 
        pd.DataFrame(mchs["002"], index=["002"]*mchs["002"].size, columns=["value"]), 
        pd.DataFrame(mchs["003"], index=["003"]*mchs["003"].size, columns=["value"]), 
        pd.DataFrame(mchs["004"], index=["004"]*mchs["004"].size, columns=["value"]), 
        pd.DataFrame(mchs["005"], index=["005"]*mchs["005"].size, columns=["value"]), 
        pd.DataFrame(mchs["006"], index=["006"]*mchs["006"].size, columns=["value"]), 
    ])
    #%%
    mchs_df["mch_id"] = mchs_df.index.tolist()
    #%%
    temp = chamber2chamber(mchs_df, col_groupby="mch_id", col_value="value")
#%%
