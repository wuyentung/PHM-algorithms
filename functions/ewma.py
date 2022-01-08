import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def ewma(phase1_list, phase2_list, alpha, L, stitle, xlabel, ylabel, path=""):
  
#     計算control limits
    z0 = np.mean(phase1_list)
    sigma = np.std(phase1_list)
    lcl = []
    ucl = []
    for i in range(len(phase2_list)):

        lcl.append(float(z0 - L*sigma*((alpha/(2-alpha))*(1-(1-alpha)**(2*i)))**0.5))

        cl = float(z0)

        ucl.append(float(z0 + L*sigma*((alpha/(2-alpha))*(1-(1-alpha)**(2*i)))**0.5))
        
#     計算EWMA值
    z = []
    time = []
    z.append(z0)
    for i in range(len(phase2_list)):
        z.append(alpha*(phase2_list[i])+(1-alpha)*z[i])
        time.append(i)
    z.pop(0)
        
#     繪圖 
#     figsize:圖片大小, dpi:解析度, linewidth:線條寬度, color:線條顏色, markersize:點大小, label:線段標示, fontsize:字大小, labelpad:標籤和 x 軸之間的間距
    plt.figure(figsize=(200,100),dpi=100,linewidth = 20)
    plt.plot(time,z,color = 'k', marker='o',markersize = 50, label="value",linewidth =20)
    plt.title(f"{stitle}", fontsize=150)
    plt.xticks(fontsize=100)
    plt.yticks(fontsize=100)
    plt.xlabel(f"{xlabel}", fontsize=100, labelpad = 15)
    plt.ylabel(f"{ylabel}", fontsize=100, labelpad = 20)
    plt.legend(loc = "best", fontsize=100)
    plt.plot(time, ucl[0:len(time)], color = 'r', linewidth = 20)
    plt.plot(time, lcl[0:len(time)], color = 'r', linewidth = 20)
    plt.savefig(f"{path}{stitle}.png")
    plt.show()
    return z
        
