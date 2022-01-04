import pandas as pd
import numpy as np
import matplotlib as plt


def ewma(phase1_list, phase2_list, alpha, L, stitle, xlabel, ylabel, path=""):
                    
    z0 = np.mean(phase1_list)
    sigma = np.std(phase1_list)
    lcl = []
    ucl = []

    for i in range(len(phase2_list)):

        lcl.append(float(z0 - L*sigma*((alpha/(2-alpha))*(1-(1-alpha)**(2*i)))**0.5))

        cl = float(z0)

        ucl.append(float(z0 + L*sigma*((alpha/(2-alpha))*(1-(1-alpha)**(2*i)))**0.5))

    z = []
    time = []
    z.append(z0)

    for i in range(len(phase2_list)):
        z.append(alpha*(phase2_list[i])+(1-alpha)*z[i])
        time.append(i)

    z.pop(0)
        
    plt.figure(figsize=(200,100),dpi=100,linewidth = 20)
    plt.plot(time,z,'s-',color = 'r', marker='o',markersize = 50, label="value",linewidth =20)
    plt.title('%s' %stitle, fontsize=150)
    plt.xticks(fontsize=100)

    plt.yticks(fontsize=100)
    plt.xlabel("%s" %xlabel, fontsize=100, labelpad = 15)
    plt.ylabel("%s" %ylabel, fontsize=100, labelpad = 20)
    plt.legend(loc = "best", fontsize=100)

    plt.plot(time, ucl[0:len(time)], "k-", linewidth = 20)
    plt.plot(time, lcl[0:len(time)], "k-", linewidth = 20)

    return z
        
