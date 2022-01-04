import pandas as pd
import numpy as np
import scipy as sc
import matplotlib as plt
from scipy import stats

def hotelling_t2(phase1_df, phase2_df, alpha, stitle, xlabel, ylabel, path=""):

    out = []
    for i in range(len(phase1_df)):
        #difference matrix for v
        v = phase1_df.diff()[1:] 

        s = np.cov(phase1_df.T)

        x = np.array((phase1_df - phase1_df.mean()).iloc[i]).reshape(-1,1)

        t = np.dot(x.T,np.linalg.inv(s))
        t = np.dot(t,x)[0][0]
        out.append(t)
    m,f = phase2_df.shape
    alpha=alpha
    q = (2*((m-1)**2)) / (3*m-4)

    ucl = float(((m - 1) * (m - 1) / m)* (stats.beta(f / 2, ((m - f - 1) / 2)).ppf(1-alpha/2)),)

    plt.figure(figsize=(10,8))
    plt.title('Hotelling t2 with confidence'+str(alpha))
    plt.plot(out,'go--',color='b')
    plt.axhline(y = ucl,color='red',ls='--',label='UCL')
    plt.legend()
    plt.show()
    return out
