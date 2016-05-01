# -*- coding: utf-8 -*-
"""
Created on Wed Jan 06 00:08:15 2016

@author: MITHIL
"""
import matplotlib.pyplot as plt
import scipy
import scipy.integrate 
class heatexchanger:
   
   Ma=1.0#Mass of hot fluid
   Mb=2.0#MAss of cold fluid
   L=10.0#length of HE
   P=10.0
   U=100.0#overall heat transfer coeff.
   TempAin=400.0#inlet temperature of hot fluid
   TempBout=300.0#outlet temperature of cold fluid
   k=10
   Cpa=lambda v: 4000+0.1*(v)+0.01*(v*v)
   Cpb=lambda u: 3000+0.2*(u)+0.05*(u*u)
   T=1.0
           
   TempB_o=range(k+1)
   TempA_i=range(k+1)
   def hot_1(self,x,y):#x and y are the temperatures of hot and cold fluid 
                Cph=4000+0.1*(x)+0.01*(x*x)#specific heat capacity of hot fluid
                Dh=(self.P*self.U*(x-y))/(self.Ma*Cph)#Dt/dx for hot fluid
                return Dh
   def cold_1(self,x,y):
                Cpc=3000+0.2*(y)+0.05*(y*y)
                Dc=(self.P*self.U*(x-y)/(self.Mb*Cpc))
                return Dc
   def calc_1(self,x,y,k):
                
                TempA=range(k+1)
                TempB=range(k+1)
                TempA[0]=400.0
                TempB[0]=350.0
                for i in range(k):
                    Dh=self.hot_1(x,y)
                    Dc=self.cold_1(x,y)
                    x = x-Dh*(self.L/(k-1))
                    y= y-Dc*(self.L)/(k-1)
                    TempA[i+1]=x
                    TempB[i+1]=y
                    TempB_guess1=TempB[k]
                return TempB_guess1
   def hot_2(self,a,b):#x and y are the temperatures of hot and cold fluid 
                Cph=4000+0.1*(a)+0.01*(a*a)#specific heat capacity of hot fluid
                Dh=(self.P*self.U*(a-b))/(self.Ma*Cph)#Dt/dx for hot fluid
                return Dh
   def cold_2(self,a,b):
                Cpc=3000+0.2*(b)+0.05*(b*b)
                Dc=(self.P*self.U*(a-b)/(self.Mb*Cpc))
                return Dc
   def calc_2(self,a,b,k):
                
                TempC=range(k+1)
                TempD=range(k+1)
                TempC[0]=400.0
                TempD[0]=320.0
                for i in range(k):
                    Dh=self.hot_2(a,b)
                    Dc=self.cold_2(a,b)
                    a = a-Dh*(self.L/(k-1))
                    b= b-Dc*(self.L)/(k-1)
                    TempC[i+1]=a
                    TempD[i+1]=b
                    TempB_guess2=TempD[k]
                return TempB_guess2
   def final_1(self,x,y,a,b,k):
                TempB_guess1=self.calc_1(x,y,k)
                TempB_guess2=self.calc_2(a,b,k)
                TempB_out=350.0+(30.0*(300.0-TempB_guess1)/(TempB_guess1-TempB_guess2))
                return TempB_out
                print TempB_out
   def final_2(self,x,y,a,b,k):
                
                TempP=range(k+1)
                TempQ=range(k+1)
                TempP[0]=400.0
                TempQ[0]=self.final_1(x,y,a,b,k)
                for i in range(k):
                    Dh=self.hot_2(a,b)
                    Dc=self.cold_2(a,b)
                    a = a-Dh*(self.L/(k-1))
                    b= b-Dc*(self.L)/(k-1)
                    TempP[i+1]=a
                    TempQ[i+1]=b
                TempA_i1=TempP[k]
                return TempA_i1
   def result_1(self,x,y,a,b,k):
                           
                                
                for n in range(10):
                    error=range(k+1)
                    TempA_i=range(k+1)
                    TempB_o=range(k+1)
                    Cpa=self.Cpa
                    Cpb=self.Cpb
                    TempB_out=self.final_1(x,y,a,b,k)
                    TempA_i1=self.final_2(x,y,a,b,k)
                    TempA_i[k]=TempA_i1        
                    TempB_o[k]=TempB_out
                    
                    from scipy.integrate import quad
                   
                    def intgrnd1(x):
                        return 4000+0.1*x+0.01*x*x
                    result,err=quad(intgrnd1,TempA_i[k],400)
                    Ha = result
                    
                    def intgrnd2(x):
                        return (3000+0.2*x+0.05*x*x)*2
                    result,err=quad(intgrnd2,300,TempB_o[k])
                    Hb =  result
                    error[k]=(Ha-Hb)*100/Ha
                    plt.plot(k,error[k],'ro')
                    print k,TempA_i[k],TempB_o[k],Ha,Hb,error[k]
                    k=k+10
                
#                x=scipy.array(error)      
               # y=[10,20,30,40,50,6,70,80,90,100,110]
                   # plt.plot(x,y,'ro')


plt.plot()

st1=heatexchanger()
st1.result_1(400.0,350.0,400.0,320.0,10)
plt.show() 