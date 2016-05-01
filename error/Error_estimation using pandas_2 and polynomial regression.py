# -*- coding: utf-8 -*-
"""
Created on Tue Feb 09 00:18:12 2016

@author: Omkar Mehta
"""
# import formula api as alias smf
import statsmodels.formula.api as smf
import numpy as np
import pandas as pd
import statsmodels.api as sm
import os
import matplotlib.pyplot as plt
pre = os.path.dirname(os.path.realpath(__file__))
fname = 'Unsteady state.xlsx'
path = os.path.join(pre, fname)
df = pd.read_excel(path,sheetname='Set 1')
df.head()

y = df.Ydata  # response
print y.shape
X = df.x  # predictor
print X.shape
X = sm.add_constant(X)  # Adds a constant term to the predictor
X.head()

# plot x vs Ydata
plt.figure(figsize=(6 * 1.618, 6))
plt.scatter(df.x, df.Ydata, s=10, alpha=0.3)
plt.xlabel('x')
plt.ylabel('Ydata')

# points linearlyd space on lstats
x = pd.DataFrame({'x': np.linspace(df.x.min(), df.x.max(), 100)})

# 1-st order polynomial
poly_1 = smf.ols(formula='Ydata ~  x-1', data=df).fit()
plt.plot(x.x, poly_1.predict(x), 'b-', label='Poly n=1 $R^2$=%.2f' % poly_1.rsquared, 
         alpha=0.9)
a=poly_1.summary()
# 2-nd order polynomial
poly_2 = smf.ols(formula='Ydata ~ 1 + x + I(x ** 2.0)', data=df).fit()
plt.plot(x.x, poly_2.predict(x), 'g-', label='Poly n=2 $R^2$=%.2f' % poly_2.rsquared, 
         alpha=0.9)
b=poly_2.summary()
# 3-rd order polynomial
poly_3 = smf.ols(formula='Ydata ~ 1 + x + I(x ** 2.0) + I(x ** 3.0)', data=df).fit()
plt.plot(x.x, poly_3.predict(x), 'r-', alpha=0.9,
         label='Poly n=3 $R^2$=%.2f' % poly_3.rsquared)
c=poly_3.summary()
plt.legend()
print 'a', a
print 'b',b
print 'c',c