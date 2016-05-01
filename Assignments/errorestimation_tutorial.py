# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 11:11:45 2016

@author: Omkar Mehta
"""
# various libraries imported for analysis of curvefitting
import scipy,numpy
import scipy.optimize,scipy.stats
import numpy.random
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels
import statsmodels.stats
import statsmodels.stats.stattools as stools
import os
plt.style.use("ggplot")

#code to format axis
def formataxis(ax):
	ax.xaxis.label.set_fontname('Georgia')
	ax.xaxis.label.set_fontsize(12)
	ax.yaxis.label.set_fontname('Georgia')
	ax.yaxis.label.set_fontsize(12)	
	ax.title.set_fontname('Georgia')
	ax.title.set_fontsize(12)
	
	for tick in ax.xaxis.get_major_ticks():
		tick.label.set_fontsize(8)
	for tick in ax.yaxis.get_major_ticks():
		tick.label.set_fontsize(8)

#code to calculate standard error of fit
def get_stderr_fit(f,Xdata,popt,pcov):
	Y=f(Xdata,popt)
	listdY=[]
	for i in xrange(len(popt)):
		p=popt[i]
		dp=abs(p)/1e6+1e-20
		popt[i]+=dp
		Yi=f(Xdata,popt)
		dY=(Yi-Y)/dp
		listdY.append(dY)
		popt[i]-=dp
	listdY=scipy.array(listdY)
	#listdY is an array with N rows and M columns, N=len(popt), M=len(xdata[0])
	#pcov is an array with N rows and N columns
	left=scipy.dot(listdY.T,pcov) 
	#left is an array of M rows and N columns
	right=scipy.dot(left,listdY)
	#right is an array of M rows and M columns
	sigma2y=right.diagonal()
	#sigma2y is standard error of fit and function  of X
	mean_sigma2y=scipy.mean(right.diagonal())
	M=Xdata.shape[1];print M
	N=len(popt);print N
	avg_stddev_data=scipy.sqrt(M*mean_sigma2y/N)
	#this is because if exp error is constant at sig_dat,then mean_sigma2y=N/M*sig_dat**2
	sigmay=scipy.sqrt(sigma2y)
	return sigmay,avg_stddev_data

	
def fitdata(f,Xdata,Ydata,Errdata,pguess,ax=False,ax2=False):
	'''
	fitdata(f,Xdata,Ydata,Errdata,pguess):
	'''
	def error(p,Xdata,Ydata,Errdata):
		Y=f(Xdata,p)
		residuals=(Y-Ydata)/Errdata
		return residuals
	res=scipy.optimize.leastsq(error,pguess,args=(Xdata,Ydata,Errdata),full_output=1)
	(popt,pcov,infodict,errmsg,ier)=res   #optimize p
	perr=scipy.sqrt(scipy.diag(pcov))    #vector of sd of p
	M=len(Ydata)
	N=len(popt)
	#Residuals
	Y=f(Xdata,popt)
	residuals=(Y-Ydata)/Errdata
	meanY=scipy.mean(Ydata)
	squares=(Y-meanY)/Errdata
	squaresT=(Ydata-meanY)/Errdata
	
	SSM=sum(squares**2) #corrected sum of squares
	SSE=sum(residuals**2)  #sum of squares of errors
	SST=sum(squaresT**2)  #total corrected sum of squares
	
	DFM=N-1   #for model
	DFE=M-N   #for error
	DFT=M-1   #total
	
	MSM=SSM/DFM #mean squares for model(explained variance)
	MSE=SSE/DFE #mean squares for errors(should be small wrt MSM) unexplained variance
	MST=SST/DFT #mean squares for total	
	
	R2=SSM/SST  #proportion of explained variance
	R2_adj=1-(1-R2)*(M-1)/(M-N-1) #adjusted R2
	
	#ttest to see if parameters are different from zero
	t_stat=popt/perr #tstatistic for popt different from zero
	t_stat=t_stat.real
	p_p=1.0-scipy.stats.t.cdf(t_stat,DFE) #should be low for good fit
	z=scipy.stats.t(M-N).ppf(0.95)
	p95=perr*z
	#Chisquared ananlysis on residuals
	chisquared=sum(residuals**2)
	degfreedom=M-N
	chisquared_red=chisquared/degfreedom
	p_chi2=1.0-scipy.stats.chi2.cdf(chisquared,degfreedom)
	stderr_reg=scipy.sqrt(chisquared_red)
	chisquare=(p_chi2,chisquared,chisquared_red,degfreedom,R2,R2_adj)
	
	#Analysis of residuals
	w,p_shapiro=scipy.stats.shapiro(residuals) # to check if residuals are normally distributed
	mean_res=scipy.mean(residuals)
	stddev_res=scipy.sqrt(scipy.var(residuals))
	t_res=mean_res/stddev_res
	p_res=1.0-scipy.stats.t.cdf(t_res,M-1)
	#if p_res<0.05,null hypothesis is rejected.
	#R^2>0 and at least one of the fitting parameters>0
	#F-test on residuals
	F=MSM/MSE
	p_F=1.0-scipy.stats.f.cdf(F,DFM,DFE)
	
	dw=stools.durbin_watson(residuals) #to check if they are correlated
	resanal=(p_shapiro,w,mean_res,p_res,F,p_F,dw)
	
	if ax:
		formataxis(ax)
		ax.plot(Ydata,Y,'ro')
		ax.errorbar(Ydata,Y,yerr=Errdata,fmt='.')
		Ymin,Ymax=min((min(Y),min(Ydata))),max((max(Y),max(Ydata)))
		ax.plot([Ymin,Ymax],[Ymin,Ymax],'b')
		
		ax.xaxis.label.set_text('Data')
		ax.yaxis.label.set_text('Fitted')
		sigmay,avg_stddev_data=get_stderr_fit(f, Xdata, popt, pcov)
		Yplus=Y+sigmay
		Yminus=Y-sigmay
		ax.plot(Y,Yplus,'c',alpha=.6,linestyle='--',linewidth=.5)
		ax.plot(Y,Yminus,'c',alpha=.6,linestyle='--',linewidth=.5)
		ax.fill_between(Y,Yminus,Yplus,facecolor='cyan',alpha=.5)
		titletext='Parity plot for fit.\n'
		titletext+=r'$r^2$=%5.2f,$r^2_{adj}$=%5.2f, '
		titletext+='$\sigma_{exp}$=%5.2f,$\chi^2_{\nu}$=%5.2f,$p_{\chi^2}$=%5.2f, '
		titletext+='$\sigma_{err}^{reg}$=%5.2f'
		ax.title.set_text(titletext%(R2,R2_adj,avg_stddev_data,chisquared_red,p_chi2,stderr_reg))
		ax.figure.canvas.draw()
	
	if ax2:#test for homoscedasticity
		formataxis(ax2)
		ax2.plot(Y,residuals,'ro')
		
		ax2.xaxis.label.set_text('Fitted data')
		ax2.yaxis.label.set_text('Residuals')
		
		titletext='Analysis of residuals\n'
		titletext+=r'mean=%5.2f,$p_{res}$=%5.2f,$p_{shapiro}$=%5.2f,$Durbin-Watson$=%2.1f'
		titletext+='\n F=%5.2f,$p_F$=%3.2e'
		ax2.title.set_text(titletext%(mean_res,p_res,p_shapiro,dw,F,p_F))
		
		ax2.figure.canvas.draw()
		
	return popt,pcov,perr,p95,p_p,chisquare,resanal

#Code for importing data from an excel file and preparing it for fitting
'''def import_data(xlfile,sheetname):
	pre = os.path.dirname(os.path.realpath(__file__))
	fname = 'xlfile'
	path = os.path.join(pre, fname)
	df = pd.read_excel(path,sheetname=sheetname)
	return df'''
def prepare_data(df,Criterion,Predictors,Error=False):
	Y=scipy.array(df[Criterion])
	if Error:
		Errdata=scipy.array(df[Error])
	else:
		Errdata=scipy.ones(len(Y))
	Xdata=[]
	for X in Predictors:
		X=list(df[X])
		Xdata.append(X)
	Xdata=numpy.array(Xdata)
	return Xdata,Y,Errdata

if __name__=="__main__":
	fig=plt.figure()
	ax=fig.add_subplot(111)
	fig.show()
	
	fig2=plt.figure()
	ax2=fig2.add_subplot(111)
	fig2.show()
	#Make arbitrary function of three variables
	def f(X,p):
		(x,)=X
		Y=p[0]*x
		return Y
	#get data from excel file using pandas
	pre = os.path.dirname(os.path.realpath(__file__))
	fname = 'Ball valve.xlsx'
	path = os.path.join(pre, fname)
	df = pd.read_excel(path,sheetname='Data')
	'''df=import_data('Ball valve.xlsx','Data')'''
	Xdata,Ydata,Errdata=prepare_data(df,'Ydata',('x',),Error='err')
	#Initial Guess
	N=1
	pguess=N*[0.0]
	
	popt,pcov,perr,p95,p_p,chisquare,resanal=fitdata(f,Xdata,Ydata,Errdata,pguess,ax=ax,ax2=ax2)
	print 'popt=',popt
	print 'p_p=',p_p ,',since p_p is less than .05, null hypothesis is rejected.'
	print 'p_res=',resanal[3]

import numpy as np
import pandas as pd
import statsmodels.api as sm
import os
pre = os.path.dirname(os.path.realpath(__file__))
fname = 'Ball valve.xlsx'
path = os.path.join(pre, fname)
df = pd.read_excel(path,sheetname='Data')
df.head()

y = df.Ydata  # response
X = df.x  # predictor
X = sm.add_constant(X)  # Adds a constant term to the predictor
X.head()

est = sm.OLS(y, X)
est = est.fit()
a=est.summary()
print a
