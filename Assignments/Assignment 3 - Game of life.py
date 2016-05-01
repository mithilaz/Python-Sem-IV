# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 15:19:47 2016

@author: Omkar Mehta
"""

import math
import scipy.optimize
import numpy
from scipy.integrate import odeint
import pylab
from scipy.optimize import curve_fit

#0=CO2,1=CH4,2=H2O these subscripts denote Components
a=1.5 #1/m -->surface area per unit volume of packing
kl=.0001 #m/s-->liquid phase mass transfer coefficient
kg=.0000001 #gmol/(m2.s.Pa)-->gas phase mass transfer coefficient
P=101325.0 #Pa-->atmospheric pressure
T=298.16 #K-->Operating temperature
A=10.0 #m2-->Area of column
rho=float(1000/18) #gmol/m3-->molar density
z=numpy.linspace(.0,10,100) #length of the column
H=[101325/34,101325/1.4] #Henry's constant
C1=73.649;C2=-7258.2;C3=-7.3037;C4=4.1653*10**-6;C5=2 #constants to calculate Psat of water
#WATER P=Pa T=K
Psat=scipy.exp(C1+(C2/T)+(C3*scipy.log(T))+(C4*T**C5))

#Defining function to integrate it using odeint later on
def dNdt(N,z):
    dL0dz=kl*a*A*((P*(N[0]/(N[0]+N[1]+N[2]))*(1/H[0]))-rho*N[3]/(N[3]+N[4]+N[5]))
    dG0dz=kl*a*A*((P*(N[0]/(N[0]+N[1]+N[2]))*(1/H[0]))-rho*N[3]/(N[3]+N[4]+N[5]))
    dL1dz=kl*a*A*((P*(N[1]/(N[0]+N[1]+N[2]))*(1/H[1]))-rho*N[4]/(N[3]+N[4]+N[5]))
    dG1dz=kl*a*A*((P*(N[1]/(N[0]+N[1]+N[2]))*(1/H[1]))-rho*N[4]/(N[3]+N[4]+N[5]))
    dL2dz=-kg*a*A*(Psat-(P*N[0]/(N[0]+N[1]+N[2])))
    dG2dz=-kg*a*A*(Psat-(P*N[0]/(N[0]+N[1]+N[2])))
    return numpy.array([dG0dz,dG1dz,dG2dz,dL0dz,dL1dz,dL2dz])


# inlet gas moles to the bottom
alpha=[.5,.5,0.0]
#entering water moles at the top
beta=[.0,.0,1.0]

#initial guess value of moles in liquid.
gamma1=[.05,.05,.09];
#first initial bottom moles
Ninit1=numpy.concatenate((alpha,gamma1),axis=0)
#solving differential eqns using odeint
N1=odeint(dNdt,Ninit1,z):
#Gas moles and liquid moles
GN1=N1[-1,:3];LN1=N1[-1,3:]

#second initial guess value of moles in liquid.
gamma2=[.04,.04,.092]
#second initial bottom moles
Ninit2=numpy.concatenate((alpha,gamma2),axis=0)
#solving differential eqns using odeint
N2=odeint(dNdt,Ninit2,z)
#Gas moles and liquid moles
GN2=N2[-1,:3];LN2=N2[-1,3:]

#third initial guess value of moles in liquid.
gamma3=[.03,.03,.094]
#third initial bottom moles
Ninit3=numpy.concatenate((alpha,gamma3),axis=0)
#solving differential eqns using odeint
N3=odeint(dNdt,Ninit3,z)
#Gas moles and liquid moles
GN3=N3[-1,:3];LN3=N3[-1,3:]

#generating xdata and ydata for curvefitting
xdata1=[gamma1[0],gamma2[0],gamma3[0]]
ydata1=[LN1[0],LN2[0],LN2[0]]
def f1(x,a1,b1):
    return -a1*x+b1
popt1,pcov1=curve_fit(f1,xdata1,ydata1)
r=(beta[0]-popt1[1])/popt1[0]

xdata2=[gamma1[1],gamma2[1],gamma3[1]]
ydata2=[LN1[1],LN2[1],LN2[1]]
def f2(x,a2,b2):
    return -a2*x+b2
popt2,pcov2=curve_fit(f2,xdata2,ydata2)
s=(beta[1]-popt2[1])/popt2[0]

xdata3=[gamma1[2],gamma2[2],gamma3[2]]
ydata3=[LN1[2],LN2[2],LN2[2]]
def f3(x,a3,b3):
    return -a3*x+b3

#using curvefit
popt3,pcov3=curve_fit(f3,xdata3,ydata3)
t=(beta[0]-popt3[1])/popt3[0]

#final answer
gamma=numpy.array([r,s,t])
Ninit=numpy.concatenate((alpha,gamma),axis=0)
N=odeint(dNdt,Ninit,z)

print("At z=10m, the moles GCO2,GCH4,GH2O,LCO2,LCH4.LH2O", N[-1])
print("At z=0m, the moles GCO2,GCH4,GH2O,LCO2,LCH4.LH2O", N[0])
print('H20 in liquid',N[:,5])
print('H2O in Gas',N[:,2])
print('CH4 in liquid',N[:,4])
print('CH4 in gas',N[:,1])
print('CO2 in liquid',N[:,3])
print('CO2 in gas',N[:,0])

pylab.plot(z,N[:,5],label='H2O in liquid')
pylab.show()
pylab.plot(z,N[:,2],label='H2O in Gas')
pylab.show()
pylab.plot(z,N[:,4],label='CH4 in liquid')
pylab.show()
pylab.plot(z,N[:,1],label='CH4 in Gas')
pylab.show()
pylab.plot(z,N[:,3],label='CO2 in liquid')
pylab.show()
pylab.plot(z,N[:,0],label='CO2 in Gas')
pylab.legend()
pylab.show()
"""References
1.Coefficients obtained from Perry's handbook
2.From Sim lab folder, Henry-3.0.pdf"""