# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 15:33:43 2016

@author: Archit Datar
"""

    

import scipy, numpy
import scipy.optimize,scipy.stats
import numpy.random
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels
import statsmodels.stats
import statsmodels.stats.stattools as stools

plt.style.use("ggplot")

def formataxis(ax):
    ax.xaxis.label.set_fontname("Georgia")
    ax.xaxis.label.set_fontsize(12)
    ax.yaxis.label.set_fontname("Georgia")
    ax.yaxis.label.set_fontsize(12)
    ax.title.set_fontname("Georgia")
    ax.title.set_fontsize(12)
    
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(8)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(8)

def get_stderr_fit(f,Xdata,popt,pcov):
    
   Y= f(Xdata, popt)
   listdY=[]
   for i in xrange(len(popt)):
       p=popt[i]
       dp= abs(p)/1e6+1e-20
       popt[i]+=dp
       Yi= f(Xdata, popt)
       dY= (Yi-Y)/dp
       listdY.append(dY)
       popt[i]-=dp
   listdY= scipy.array(listdY)
   #list dy is the d in the derivation. it has N X M
   #pcov is N X N
   
   left= scipy.dot(listdY.T,pcov)
   right=scipy.dot(left,listdY)
   
   sigma2y= right.diagonal()
   #sigma2y is a standard function of fit
   mean_sigma2y= scipy.mean(right.diagonal())
   
   M= Xdata.shape[0]
   N= len(popt)
   avg_stddev_data=scipy.sqrt(M*mean_sigma2y/N)
   sigmay= scipy.sqrt(sigma2y)
   return sigmay,avg_stddev_data
   
def fitdata(f,Xdata,Ydata,Errdata,pguess,ax= False,ax2= False):
    
    #calculating the popt 
    
    def error(pguess,Xdata,Ydata,Errdata):
        Y=f(Xdata,pguess)
        residuals= (Y-Ydata)/Errdata
        return (residuals)
    
    res= scipy.optimize.leastsq(error, pguess,args=(Xdata,Ydata,Errdata),full_output=1)
      
    (popt,pcov,infodict,errmsg,ier)=res
      
    perr= scipy.sqrt(scipy.diag(pcov))
    
    M= len(Xdata)
    N= len(popt)
   #residuals
    Y= f(Xdata,popt)
    residuals=(Y-Ydata)/Errdata
    meanY= scipy.mean(Ydata)
    squares= (Y-meanY)/Errdata
    squaresT= (Ydata-meanY)/Errdata
    
    SSM= sum(squares**2)#corrected sum of squares
    SSE= sum(residuals**2)#sum of squares of errors
    SST= sum(squaresT**2)#total corrected sum of squrare

    DFM= N-1
    DFE= M-N
    DFT= M-1

    MSM= SSM/DFM
    MSE= SSE/DFE
    MST= SST/DFT

    R2= SSM/SST    #proportion of explained variance
    R2_adj= 1-(1-R2)*(M-1)/(M-N-1)#Adjusted R2 

    # t test to see if parameters are different from 0
    t_stat= popt/perr
    t_stat= t_stat.real
    p_p= 1.0-scipy.stats.t.cdf(t_stat,DFE)
    z=scipy.stats.t(M-N).ppf(0.95)
    p95= perr*z

    #chisquared analysis on residuals
    chisquared= sum(residuals**2)
    degfreedom= M-N
    chisquared_red= chisquared/degfreedom
    p_chi2= 1.0-scipy.stats.chi2.cdf(chisquared,degfreedom)       
    stderr_reg= scipy.sqrt(chisquared_red)
    chisquare=(p_chi2, chisquared,chisquared_red,degfreedom,R2,R2_adj)
    
    #analysis of residuals
    w,p_shapiro= scipy.stats.shapiro(residuals)
    mean_res= scipy.mean(residuals)
    stddev_res= scipy.sqrt(scipy.var(residuals))
    t_res= mean_res/stddev_res 
    p_res=1.0-scipy.stats.t.cdf(t_res,M-1)
    #if p<0.05, null hypothesis is rejected and mean is non-zero
    #should be high for a good fit
    
    #F-test on the residuals
    F= MSM/MSE #explained variance/ unexplained should be large
    p_F= 1.0-scipy.stats.f.cdf(F,DFM,DFE)
    #if p_F<0.05, null hypo is rejected
    dw= stools.durbin_watson(residuals)
    resanal= (p_shapiro,w,mean_res,p_res,F,p_F,dw)
    
    if ax:
        formataxis(ax)
        ax.plot(Ydata,Y,'ro')
        ax.errorbar(Ydata,Y,yerr=Errdata,fmt='.')
        Ymin, Ymax= min((min(Y),min(Ydata))),max((max(Y),max(Ydata)))
        ax.plot([Ymin,Ymax],[Ymin,Ymax],'b')
        
        ax.xaxis.label.set_text('Data')
        ax.yaxis.label.set_text('Fitted')
        
        sigmaY, avg_stddev_data= get_stderr_fit(f,Xdata,popt,pcov)
        Yplus= Y+sigmaY
        Yminus= Y-sigmaY
        ax.plot(Y,Yplus,'c',alpha=0.6,linestyle='--',linewidth= 0.5)
        ax.plot(Y,Yminus,'c',alpha=0.6,linestyle='--',linewidth= 0.5)
        ax.fill_between(Y,Yminus,Yplus,facecolor= 'cyan',alpha=0.5)
        titletext='Parity plot for fit.\n'
        titletext+= r'$r^r$=%5.2f,$r^2_(adj)$=%5.2f,'
        titletext+= '$\sigma_<exp>$=%5.2f,$\chi^2_<\nu>$= %5.2f,$p_<chi_2>$=%5.2f,'
        titletext+= '$sigma_<err>^<reg>$=%5.2f'
        
        ax.title.set_text(titletext%(R2,R2_adj,avg_stddev_data,chisquared_red,p_chi2,stderr_reg))
        ax.figure.canvas.draw()
        
    if ax2 :  #test for homoscedaticity  
        formataxis(ax2)
        ax2.plot(Y,residuals,'ro')
        
        ax2.xaxis.label.set_text('Fitted Data')
        ax2.yaxis.label.set_text('Residuals')
        
        titletext= 'Analysis of Residuals\n'
        titletext+= r'mean=%5.2f,$p_(res)$=%5.2f,$p_<shapiro>$= %5.2f, $Durbin-Watson$=%2.1f'
        titletext+= '\n F= %5.2f, $p_F$=%3.2e'
        ax2.title.set_text(titletext%(mean_res,p_res,p_shapiro,dw, F, p_F))
        
        ax2.figure.canvas.draw()
        
    return popt, pcov,perr,p95,p_p,chisquare,resanal



"""    
#importing data (test)
def import_data(xlfile, sheetname):
    df= pd.read_excel(xlfile,sheetname=sheetname)
    return df
    
def prepare_data(df,Criterion,Predictors,Error= False):
    Y= scipy.array(df[Criterion])
    if Error:
        Errdata= scipy.array(df[Error])
    else:
        Errdata= scipy.ones(len(Y))
    Xdata=[]
    for X in Predictors:
        X= list(df[X])
        Xdata.append(X)
    Xdata= scipy.array(Xdata)
    return Xdata,Y, Errdata
    
if __name__=="__main__":
    fig=plt.figure()
    ax=fig.add_subplot(111)
    fig.show()
    
    fig2= plt.figure()
    ax2=fig2.add_subplot(111)
    fig2.show()
    
    #make arbitrary function of three variables
    def f(X,p):
        (x,y,z)=X
        Y=p[0]+p[1]*x**2+p[2]*y+p[3]*z
        return Y
        
    #get data from excel file using pandas
    df= import_data('SynthData.xlsx','Data')
    Xdata, Ydata, Errdata= prepare_data(df,'Ydata',('x','y','z'),Error='err')"""
    
