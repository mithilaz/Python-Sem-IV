# -*- coding: utf-8 -*-
"""Libraries Imported"""

import numpy as np
import numpy
import scipy
import scipy.stats
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import pandas as pd
from numpy import log
import win32com.client

"""Constants Used"""

g=9.81
pi=numpy.pi

"""Legend"""

#h===Manometer Height Difference
#t===Time to collect 1000ml of water
#Q===1000ml
#D===Diameter of Pipe
#p===Density of Water
#L===Length of Pipe
#pp===Density Difference between chloroform and water
#m===Viscosity of Water
#A===Area of Cross Section of Pipe
#v===Linear Velocity of Water

"""Importing Data from Excel"""

xl=win32com.client.gencache.EnsureDispatch("Excel.Application")
wb=xl.Workbooks("Static Mixer.xlsx")
sheet=wb.Sheets("Sheet1")
t=sheet.Range("B4:B8").Value
t=scipy.array(t)
t=t.reshape((1,len(t)))[0]
h=sheet.Range("C4:C8").Value
h=scipy.array(h)*0.01
h=h.reshape((1,len(h)))[0]

"""Function for ErrData Computation"""

def yd(h,pp,D,p,L,Q,t):
    A=pi/4*D**2
    v=Q/A/t
    y=log(h*pp*g*D/2/p/L/v/v)
    return y

"""Observations and Data"""

#h=numpy.array([1.2,1,0.5,0.4,0.3])*0.01         #m
#t=numpy.array([35.10,44.91,66.01,85.32,190.11]) #s
Q=numpy.ones(5)*0.001                           #m^3
D=(numpy.ones(5))*0.0209                        #m
p=(numpy.ones(5))*1000                          #kg/m^3
L=(numpy.ones(5))*2.97                          #m
pp=(numpy.ones(5))*487                          #kg/m^3
m=(numpy.ones(5))*0.001                         #Pas

"""Uncertainity in different Values (Least Count)"""
    
dx=10**-15 #for calculating Errdata
dh=0.001   #Least Count of Manometer
dD=0.00001 #Least Count of Vernier Callipers
dQ=0.00001 #Least Count of Measuring Cylinder
dL=0.001   #Least Count of Ruler
dt=0.01    #Least Count of Stopwatch
dp=50.0    #Uncertainty of Density of Water
dpp=70.71  #Uncertainty of Density Difference

"""Calculation of Errdata"""

A=pi/4*D**2
v=Q/A/t
dy=((yd(h+dx,pp,D,p,L,Q,t)-yd(h-dx,pp,D,p,L,Q,t))/2/dx*dh)**2+((yd(h,pp+dx,D,p,L,Q,t)-yd(h,pp-dx,D,p,L,Q,t))/2/dx*dpp)**2+((yd(h,pp,D+dx,p,L,Q,t)-yd(h,pp,D-dx,p,L,Q,t))/2/dx*dD)**2+((yd(h,pp,D,p+dx,L,Q,t)-yd(h,pp,D,p-dx,L,Q,t))/2/dx*dp)**2+((yd(h,pp,D,p,L+dx,Q,t)-yd(h,pp,D,p,L-dx,Q,t))/2/dx*dL)**2+((yd(h,pp,D,p,L,Q+dx,t)-yd(h,pp,D,p,L,Q-dx,t))/2/dx*dQ)**2+((yd(h,pp,D,p,L,Q,t+dx)-yd(h,pp,D,p,L,Q,t-dx))/2*dt)**2
Errdata=numpy.sqrt(dy)

"""Legend for Error Analysis"""

#Errdata===Error Estimate of Ydata
#popt===Optimum Parameters for Fit
#pcov===Covariance Matrix of Fit
#perr===Standard Deviation of Parameters
#chisquare===Sum of Squares of Weighted Residuals
#chisquared_red===Reduced Chisquare Value

"""Data Preparation for fitting"""

Xdata=np.array(log(p*v*D/m))
Ydata=np.array(yd(h,pp,D,p,L,Q,t))
pguess=[0,0]

"""Function To Be Used For Fitting"""

def y(Xdata,p):
    f=p[0]*Xdata+p[1]
    return f

"""Function To Calculate The Residuals"""

def error(p,Xdata,Ydata,Errdata):
    Y=y(Xdata,p)
    residuals=(Y-Ydata)/Errdata
    return residuals
    
"""Finding Optimum Parameters"""

res=leastsq(error,pguess,args=(Xdata,Ydata,Errdata),full_output=1)
(popt,pcov,infodict,errmsg,ier)=res
perr=scipy.sqrt(scipy.diag(pcov))

"""Error Analysis (Basic Values Required)"""

M=len(Ydata) #Number of Observations
N=len(popt)  #Number of Parameters

DFM=N-1 #Degrees of Freedom of Model
DFE=M-N #Degrees of Freedom of Error
DFT=M-1 #Total Degrees of Freedom

Y=y(Xdata,popt)
Ymean=scipy.mean(Ydata)
residuals=(Y-Ydata)/Errdata
squares1=(Y-Ymean)/Errdata
squares2=(Ydata-Ymean)/Errdata

SSM=sum(squares1**2) #Sum of Squares of Regression
SSE=sum(residuals**2)#Sum od Squares of Error
SST=sum(squares2**2) #Sum of Squares Total

MSM=SSM/DFM #Mean Squares of Model
MSE=SSE/DFE #Mean Squares for Error
MST=SST/DFT #Mean of Squares Total

"""Standard Deviation of Fit"""

listdY=[]
for i in xrange(N):
    p=popt[i]
    dp=abs(p)/10**6+10**-20
    popt[i]+=dp
    Yi=y(Xdata,popt)
    dY=(Yi-Y)/dp
    listdY.append(dY)
    popt[i]-=dp
listdY=scipy.array(listdY)
left=scipy.dot(listdY.T,pcov)
right=scipy.dot(left,listdY)
sigma2y=scipy.diag(right)
mean_sigma2y=scipy.mean(sigma2y)
avg_stddev_data=scipy.sqrt(M*mean_sigma2y/N)
sigmay=scipy.sqrt(sigma2y)
    
"""Rsquare and adjusted Rsquare Value"""

R2=SSM/SST                  
R2_adj=1-(1-R2)*(M-1)/(M-N-1) #This Value Should Be Close to 1

"""T Test for Parameters"""

t_stat=popt/perr
t_stat=t_stat.real
p_p=1.0-scipy.stats.t.cdf(t_stat,DFE)
z=scipy.stats.t(M-N).ppf(0.95)
p95=perr*z

"""Chisquare Test"""

chisquared=SSE
chisquared_red=chisquared/DFE
p_chi2=1-scipy.stats.chi2.cdf(chisquared,DFE)
stderr_reg=scipy.sqrt(scipy.var(residuals))

"""F Test on Residuals"""

F=MSM/MSE #Explained/Unexplained Variance
p_F=1.0-scipy.stats.f.cdf(F,DFM,DFE)

"""T Test on Residuals"""

Rmean=scipy.mean(residuals)
stddev_R=scipy.sqrt(scipy.var(residuals))
t_res=Rmean/stddev_R
p_res=1.0-scipy.stats.t.cdf(t_res,DFE)

"""Residual Analysis Using Shapiro-Wilk Test"""

w,p_shapiro=scipy.stats.shapiro(residuals)

"""Durbin Watson Test"""

diff=numpy.ones(4)
for i in range(1,5):
    diff[i-1]=(residuals[i]-residuals[i-1])**2
dw=sum(diff)/SSE

"Plotting"

Yplus=Y+2*sigmay
Yminus=Y-2*sigmay
plt.plot(Xdata,Yplus,ls='dashed')
plt.plot(Xdata,Yminus,ls='dashed')
plt.plot(Xdata,Ydata,ls='None',marker="x")
plt.plot(Xdata,Y)
plt.title("Illustration of Standard error of Fit")
plt.show()

plt.plot(Y,Rmean*numpy.ones(5))
plt.plot(Y,stddev_R*numpy.ones(5),ls='dashed')
plt.plot(Y,-stddev_R*numpy.ones(5),ls='dashed')
plt.plot(Y,residuals,'ro')
plt.title("Residuals vs Y")
plt.show()

"""Final Report"""

print ("Correlation is log(f)=m*log(Re)+c where")
print("m is" ,popt[0],"c is" ,popt[1])
print("R2 is",R2)
print ("")
print ("T Test")
print ("Null Hypothesis")
print ("Values of the Parameters are zero")
print ("The value of p (atleast 1 should be greater than 0.05) are")
print (p_p)
print ("Null Hypothesis is Rejected")
print("")
print ("Chisquared Test")
print ("Null Hypothesis")
print ("This Fit Explains the Data")
print ("The value of reduced chisquared(should be around 1) is")
print (chisquared_red)
print ("Null Hypothesis Cannot Be Rejected")
print ("Match Betweem Observation and Estimate is in accord with the Error Variance")
print("")
print ("F Test on Residuals")
print ("Null Hypothesis")
print ("The Residuals are Normally Distributed")
print ("The value of p(should be less than 0.05) is")
print (p_F)
print ("Null Hypothesis Cannot Be Rejected")
print("")
print ("T Test on Residuals")
print ("Null Hypothesis")
print ("The Residuals are Normally Distributed")
print ("The value of p(should be greater than 0.05) is")
print (p_res)
print ("Null Hypothesis Cannot Be Rejected")
print("")
print ("Shapiro Wilk Test")
print ("Null Hypothesis")
print ("The Residuals are Normally Distributed")
print ("The value of p(should be greater than 0.05) is")
print (p_shapiro)
print ("Null Hypothesis Cannot Be Rejected")
print("")
print ("Durbin Watson Test")
print ("This Test is To Check for positive or negative Serial Correlation")
print ("The value of w(should be = 2) is")
print (dw)
print ("This Indicates Absence of AutoCorrelation")



#print R2,chisquared_red,p_shapiro,t_res,p_F,dw


















