#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 06:08:50 2019

@author: gauravsharma
"""

# =============================================================================
# https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.truncnorm.html
# https://stackoverflow.com/questions/18441779/how-to-specify-upper-and-lower-limits-when-using-numpy-random-normal
# =============================================================================

import matplotlib.pyplot as plt
from scipy import stats


#lower, upper, mu, and sigma are four parameters
lower, upper = 2, 6
mu, sigma = 4, 2

#instantiate an object X using the above four parameters,
X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)

#generate 1000 sample data
samples = X.rvs(150)

#compute the PDF of the sample data
pdf_probs = stats.truncnorm.pdf(samples, (lower-mu)/sigma, (upper-mu)/sigma, mu, sigma)

#compute the CDF of the sample data
cdf_probs = stats.truncnorm.cdf(samples, (lower-mu)/sigma, (upper-mu)/sigma, mu, sigma)

#make a histogram for the samples
plt.hist(samples, bins= 5,normed=True,alpha=0.3,label='histogram');

#plot the PDF curves 
plt.plot(samples[samples.argsort()],pdf_probs[samples.argsort()],linewidth=2.3,label='PDF curve')

#plot CDF curve        
plt.plot(samples[samples.argsort()],cdf_probs[samples.argsort()],linewidth=2.3,label='CDF curve')


#legend
plt.legend(loc='best')



# =============================================================================
# fig, ax = plt.subplots(1, 1)
# 
# a, b = 2, 6
# mean, var, skew, kurt = truncnorm.stats(a, b, moments='mvsk')
# 
# 
# x = np.linspace(truncnorm.ppf(0.01, a, b),truncnorm.ppf(0.99, a, b), 100)
# ax.plot(x, truncnorm.pdf(x, a, b), 'r-', lw=5, alpha=0.6, label='truncnorm pdf')
# 
# rv = truncnorm(a, b)
# ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')
# 
# vals = truncnorm.ppf([0.001, 0.5, 0.999], a, b)
# np.allclose([0.001, 0.5, 0.999], truncnorm.cdf(vals, a, b))
# 
# r = truncnorm.rvs(a, b, size=50)
# 
# ax.hist(r, density=True, histtype='stepfilled', alpha=0.2)
# ax.legend(loc='best', frameon=False)
# plt.show()
# plt.clf()
# =============================================================================

