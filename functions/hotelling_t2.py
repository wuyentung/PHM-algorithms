import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def hotelling_t2(phase1_df, phase2_df, alpha=0.05, stitle="Hotelling's T-sqaured Chart", xlabel="time", ylabel="t2_value", path=""):
    
#     計算t2值
    out = []
    for i in range(len(phase2_df)):
        #difference matrix for v
        v = phase2_df.diff()[1:] 
        s = np.cov(phase2_df.T)
        x = np.array((phase2_df - phase2_df.mean()).iloc[i]).reshape(-1,1)
        t = np.dot(x.T,np.linalg.pinv(s))
        t = np.dot(t,x)[0][0]
        out.append(t)
        
#     計算control limits
    m,f = phase1_df.shape
    alpha=alpha
    q = (2*((m-1)**2)) / (3*m-4)
    ucl = float(((m - 1) * (m - 1) / m)* (stats.beta(f / 2, ((m - f - 1) / 2)).ppf(1-alpha/2)),)
    
#     繪圖
#     figsize:圖片大小, dpi:解析度, linewidth:線條寬度, color:線條顏色, markersize:點大小, label:線段標示, fontsize:字大小, labelpad:標籤和 x 軸之間的間距
    plt.figure(figsize=(200,100),dpi=100,linewidth = 20)
    plt.title(f'{stitle}', fontsize=10)
    plt.plot(out,color = 'k',markersize = 50, label="value",linewidth =20)
    plt.axhline(y = ucl,color='red', linewidth=20)
    plt.xticks(fontsize=100)
    plt.yticks(fontsize=100)
    plt.xlabel(f"{xlabel}" , fontsize=100, labelpad = 15)
    plt.ylabel(f"{ylabel}", fontsize=100, labelpad = 20)
    plt.legend(loc = "best", fontsize=100)
    plt.savefig(f"{path}{stitle}.png")
    plt.show()
    return out, ucl

#%%
## unit test
if __name__ == "__main__":
    df1 = pd.DataFrame(np.random.normal(50,2,size=(100, 10)), columns=list('ABCDEFGHIJ'))
    df2_1 = pd.DataFrame(np.random.randint(0,200,size=(50, 10)), columns=list('ABCDEFGHIJ'))
    df2_2 = pd.DataFrame(np.random.randint(100,200,size=(50, 10)), columns=list('ABCDEFGHIJ'))
    df2 = pd.concat([df2_1, df2_2])
    #%%
    t2_value, ucl = hotelling_t2(phase1_df = df1, phase2_df = df2)
#%%
