# Prognostics and Health Management (PHM) Algorithms
In this repository, we introduce nonparametric method for examining machine healthiness. Including methodology to identify maintainence effectiveness with the features and PHM algorithms for uni- and multi-virate data.  
- The main.py module is the sample for user to set the parameter for each algorithm.  
- The unit test code is writen in each module, and can be precess immediately. Each module is introduced below...

## statisticalTest
In practice, the main challenge for PHM in the firest step is to identify the correlation between data and maintianence. Under the assumption that the maintianence will make machine more stable, we vidualize data and use statistical test for two slice of univirate data to check the overall correlation between each.  
Where the statistical tests are:  
|Test|Usage of Both Data|
|:---:|:---|
|t test| the mean of distribution|
|f test| the variance of distribution|
|skewness| the skewness of distribution|
|kurtosis| the kurtosis of distribution|
|KS test| check the distribution of both data is identical or not, the distribution is different if pvalue < 0.01|
|correlation| the correlation of two data|
|dtw distance| the [dynamic time wrapping](https://dtaidistance.readthedocs.io/en/latest/usage/dtw.html) distance of two data, the smaller value the closer distance|
- The visualization of two data:  
<img src="https://github.com/wuyentung/PHM-algorithms/blob/master/images/折線圖_statistical_test.png" height="500" />  
- The DTW plot:  
<img src="https://github.com/wuyentung/PHM-algorithms/blob/master/images/DTW_statistical_test.png" height="500" />  

## chamber2chamber
- chamber to chamber: comparing the standard deviation of all machines to find the unstable ones. You could take out extreme data points in advance to prevent false alarm. 

|Method|Usage|
|:---:|:---:|
|z score| detect outliers|

## x_bar_S
$\overline X$ bar S control chart is an univirate method for single machine to detect anomalies. By watching the trends of the samples, we can identify manufacturing anomaly and measurement anomaly.  
|Submethod|Usage|
|:---:|:---:|
|sliding window| detect anomaly with trend factor|

- $\overline X$ S control chart example:  
<img src="https://github.com/wuyentung/PHM-algorithms/blob/master/images/x bar with S chart.png" height="500" />  

## ewma
The EWMA control chart help us detect time-dependent data with sliding window and weights. It is univirate version in this implementation, while EWMA control chart can be used in multivirate feature once the determinant of slided data is calculated.  
- EWMA control chart example:  
<img src="https://github.com/wuyentung/PHM-algorithms/blob/master/images/EWMA Chart.png" height="500" />  

## hotelling_t2
The [Hotelling's T-squared](https://www.spcforexcel.com/knowledge/variable-control-charts/hotelling-t2-control-chart) control chart aims to identify the feature distance between multivirate data, under the assumption that the data is independently collected. Data point is regards to be anomaly once its t-squared value is too large, i.e., jump over UCL. However, Hotelling's T-squared control chart can be too sensitive if we break the assumptions of Hotelling's T-squared ([see](https://online.stat.psu.edu/stat505/lesson/7/7.2/7.2.6)).
- Hotelling's T-squared control chart example:  
<img src="https://github.com/wuyentung/PHM-algorithms/blob/to_public/images/Hotelling's%20T-sqaured%20Chart.png" height="500" />  