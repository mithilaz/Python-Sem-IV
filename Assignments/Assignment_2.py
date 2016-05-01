# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 20:01:44 2016

@author: Omkar Mehta
"""
import math
import scipy.optimize
import numpy
from scipy.integrate import odeint
import pylab

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
print Psat

#Defining function to integrate it using odeint later on
def dNdt(N,z):
    dL0dz=kl*a*A*((P*(N[0]/(N[0]+N[1]+N[2]))*(1/H[0]))-rho*N[3]/(N[3]+N[4]+N[5]))
    dG0dz=kl*a*A*((P*(N[0]/(N[0]+N[1]+N[2]))*(1/H[0]))-rho*N[3]/(N[3]+N[4]+N[5]))
    dL1dz=kl*a*A*((P*(N[1]/(N[0]+N[1]+N[2]))*(1/H[1]))-rho*N[4]/(N[3]+N[4]+N[5]))
    dG1dz=kl*a*A*((P*(N[1]/(N[0]+N[1]+N[2]))*(1/H[1]))-rho*N[4]/(N[3]+N[4]+N[5]))
    dL2dz=-kg*a*A*(Psat-(P*N[0]/(N[0]+N[1]+N[2])))
    dG2dz=-kg*a*A*(Psat-(P*N[0]/(N[0]+N[1]+N[2])))
    return numpy.array([dL0dz,dL1dz,dL2dz,dG0dz,dG1dz,dG2dz])

tol=1e-6
# inlet gas moles to the bottom
alpha=[.5,.5,0.0]
#initial guess value of moles in liquid.
gamma0=[.05,.05,.9];
#first initial bottom moles
Ninit1=numpy.concatenate((alpha,gamma0),axis=0)
#entering water moles at the top
beta=[.0,.0,1.0]
#solving differential eqns using odeint
N1=odeint(dNdt,Ninit1,z);gamma1=[.04,.04,.092]
#Gas moles and liquid moles
GN1=N1[-1,:3];LN1=N1[-1,3:]
#error after 1st guess
error=numpy.array([math.fabs(beta[0]-LN1[0]),math.fabs(beta[1]-LN1[1]),math.fabs(beta[2]-LN1[2])])
print("error with 1st shot: ",error)
#running 5 iterations changing guesses
for i in range(50):
    #second initial guess value
    Ninit2=numpy.concatenate((alpha,gamma1),axis=0)
    #solving differential eqns using odeint
    N2=odeint(dNdt,Ninit2,z)
    #Gas moles and liquid moles after 2nd guess
    GN2=N2[-1,:3] 
    LN2=N2[-1,3:]  
    #error after 2nd shot
    error=numpy.array([math.fabs(beta[0]-LN2[0]),math.fabs(beta[1]-LN2[1]),math.fabs(beta[2]-LN2[2])])
    print("error with 2nd shot: ",error)
    #setting error limits
    if (error[0]>tol,error[1]>1e-20,error[2]>1e-2):
        a2=gamma1[0]-((LN2[0]-beta[0])*(gamma1[0]-gamma0[0])/(LN2[0]-LN1[0]))
        a3=gamma1[1]-((LN2[1]-beta[1])*(gamma1[1]-gamma0[1])/(LN2[1]-LN1[1]))
        a4=gamma1[2]-((LN2[2]-beta[2])*(gamma1[2]-gamma0[2])/(LN2[2]-LN1[2]))
        gamma=[a2,a3,a4]
        gamma0[0]=gamma1[0];gamma0[1]=gamma1[1];gamma0[2]=gamma1[2]
        gamma1[0]=a2;gamma1[1]=a3;gamma1[2]=a4
    #Substituted  second initial guess
    Ninit2=numpy.concatenate((alpha,gamma),axis=0)
    def error(LN2,beta):
        e1=numpy.fabs(beta[0]-LN2[0])
        e2=numpy.fabs(beta[1]-LN2[1])
        e3=numpy.fabs(beta[2]-LN2[2])
        print(numpy.array([e1,e2,e3]))
        return numpy.array([e1,e2,e3])
print("At z=10m, the moles GCO2,GCH4,GH2O,LCO2,LCH4.LH2O", N2[-1])
print("At z=0m, the moles GCO2,GCH4,GH2O,LCO2,LCH4.LH2O", N2[0])
print('H20 in liquid',N2[:,5])
print('H2O in Gas',N2[:,2])
print('CH4 in liquid',N2[:,4])
print('CH4 in gas',N2[:,1])
print('CO2 in liquid',N2[:,3])
print('CO2 in gas',N2[:,0])
pylab.plot(z,N2[:,5],label='H2O in liquid')
pylab.show()
pylab.plot(z,N2[:,2],label='H2O in Gas')
pylab.show()
pylab.plot(z,N2[:,4],label='CH4 in liquid')
pylab.show()
pylab.plot(z,N2[:,1],label='CH4 in Gas')
pylab.show()
pylab.plot(z,N2[:,3],label='CO2 in liquid')
pylab.show()
pylab.plot(z,N2[:,0],label='CO2 in Gas')
pylab.legend()
pylab.show()
"""References
1.Coefficients obtained from Perry's handbook
2.From Sim lab folder, Henry-3.0.pdf"""