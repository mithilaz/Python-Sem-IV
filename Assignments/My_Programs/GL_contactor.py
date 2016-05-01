# -*- coding: utf-8 -*-
"""


@author: MITHIL
"""
import matplotlib.pyplot as plt
import scipy
import matplotlib.image as mpimg
import numpy as np

class contactr():
    #Packed column counter-current G-L contactor solver
    #data given : inlet liquid compositon x(co2),x(c2h4),x(water)=0.0,0.0,1.0
                #inlet gas coompositon  x(co2),x(c2h4),x(water)=0.5,0.5,0.0
    #assumptions inlet liquid flow rate = 100 moles per sec
                #inlet gas flow rate = 100 moles per sec
    #Guess value 1 : outlet composition of liquid L(co2),L(c2h4),L(water) = 25.0,25.0,50.0 moles per sec
    #Guess value 2 :  outlet composition of liquid L(co2),L(c2h4),L(water) = 30.0,40.0,30.0 moles per sec
    l=1.0#length of column in m
    r=0.05642#radius of column in m
    A=0.01#area of cross-section of column in sq. m
    
    P=1.0#pressure in atm
    T=25.0#temperature in celsius
    h=0.0526#step size in m
    Pw=3581.42#saturated vapour pressure of water 
              #using antoine equation : p=exp(a-b/(T+c))
              #a,b,c for water are obtained from perry`s handbook seventh edition,table13-4

    def gas_1(self,x,y,z,a,b,c):#method for change of concentration of carbon dioxide in gas stream
        A=self.A                #x-gas flow rate of carbon dioxide in moles per sec
        h=self.h                #y-gas flow rate of ethylene in moles per sec
        Pw=self.Pw              #z-gas flow rate of water in moles per sec
                                #a-liquid flow rate of carbon dioxide in moles per sec
                                #b-liquid flow rate of ethylene in moles per sec
                                #c-liquid flow rate of water in moles per sec
        Da=0.015*A*h*((101300*x/((x+y+z)*29.412))-(a/(A*1000*h)))#change in concentration of carbon dioxide in mole per sec per m
        return Da                                                #29.412 is the henrys constant in Pa/M for carbon dioxde obtained from http://www.henrys-law.org/henry-3.0.pdf
                                                                 #0.015 is kl*a in per sec  obtained from perry`s handbook seventh edition,table23-9
    def gas_2(self,x,y,z,a,b,c):#method for change in concentration of ethylene
       A=self.A
       h=self.h
       Pw=self.Pw
       Db=((101300*y/((x+y+z)*212.767))-(b/(A*1000*h)))*A*h*0.025#change in concentration of ethylene in mole per sec per m
       return Db                                                 #212.767 is the henrys constant in Pa/M  for ethylene obtained from http://www.henrys-law.org/henry-3.0.pdf
                                                                  #0.025 is kl*a in per sec  obtained from perry`s handbook seventh edition,table13-4
    def gas_3(self,x,y,z,a,b,c):#method for change in concentration of water
        A=self.A
        h=self.h
        Pw=self.Pw
        Dc=((101300*z/(x+y+z))-Pw)*A*h*0.0352#0.0352 is kg*a in per sec  obtained from perry`s handbook seventh edition,table23-9
        return Dc
    def liquid_1(self,x,y,z,a,b,c):#change in concentration of carbon dioxide in liquid
        A=self.A
        h=self.h
        Pw=self.Pw
        Dd=((101300*x/((x+y+z)*29.412)-(a/(A*1000*h))))*A*h*0.015
        return Dd
    def liquid_2(self,x,y,z,a,b,c):#change in concentration of ethylene in liquid
        A=self.A
        h=self.h
        Pw=self.Pw
        De=((101300*y/((x+y+z)*212.767)-(b/(1000*A*h))))*A*h*0.025   
        return De
    def calc_1(self,x,y,z,a,b,c):#to calculate composition of liquid inlet using first guess of liquid outlet
        La1=range(21)
        Lb1=range(21)
        Lc1=range(21)
        Ga1=range(21)
        Gb1=range(21)
        Gc1=range(21)
        
        for i in range(20):
            Da=self.gas_1(x,y,z,a,b,c)
            Db=self.gas_2(x,y,z,a,b,c)
            Dc=self.gas_3(x,y,z,a,b,c)
            Dd=self.liquid_1(x,y,z,a,b,c)
            De=self.liquid_2(x,y,z,a,b,c)
            x=x-Da
            y=y-Db
            z=z-Dc
            a=a-Dd
            b=b-De
            c=c+z
            La1[i+1]=a
            Lb1[i+1]=b
            Lc1[i+1]=c
            Ga1[i+1]=x
            Gb1[i+1]=y
            Gc1[i+1]=z
        La_guess1=La1[20]
        L_guess1=Lc1[20]
        Lb_guess1=Lb1[20]
        return L_guess1
    def calc_2(self,x,y,z,a,b,c):#to calculate liquid inlet using second guess of liquid outlet
        La2=range(21)
        Lb2=range(21)
        Lc2=range(21)
        Ga2=range(21)
        Gb2=range(21)
        Gc2=range(21)
        a=30.0
        b=20.0
        c=40.0
        for i in range(20):
            Da=self.gas_1(x,y,z,a,b,c)
            Db=self.gas_2(x,y,z,a,b,c)
            Dc=self.gas_3(x,y,z,a,b,c)
            Dd=self.liquid_1(x,y,z,a,b,c)
            De=self.liquid_2(x,y,z,a,b,c)
            x=x-Da
            y=y-Db
            z=z-Dc
            a=a-Dd
            b=b-De
            c=c+z
            La2[i+1]=a
            Lb2[i+1]=b
            Lc2[i+1]=c
            Ga2[i+1]=x
            Gb2[i+1]=y
            Gc2[i+1]=z  
        L_guess2=Lc2[20]
        La_guess2=La2[20]
        Lb_guess2=Lb2[20]
        return L_guess2
            
            
    def final(self,x,y,z,a,b,c):#to calculate final composition of gas and liquid outlet
        La_guess1=self.calc_1(x,y,z,a,b,c)
        La_guess2=self.calc_2(x,y,z,a,b,c)
        L_guess1=self.calc_1(x,y,z,a,b,c)
        L_guess2=self.calc_2(x,y,z,a,b,c)
        Lb_guess1=self.calc_1(x,y,z,a,b,c)
        Lb_guess2=self.calc_2(x,y,z,a,b,c)
        L_out=40.0+(10*(100-L_guess2)/(L_guess1-L_guess2))#to adjust the value of guess so that liquid inlet of water comes to 100
        La_out=30.0+(5*(0-La_guess2)/(La_guess1-La_guess2))#to adjust the value of guess so that liquid inlet of carbon dioxide comes to 0
        Lb_out=40.0+(5*(0-Lb_guess1)/(Lb_guess1-Lb_guess2))#to adjust the value of guess so that liquid inlet of ethylene comes to 0
        Ga3=0.0+50.0-La_out#mass balance to calculate outlet gas flow rate of carbon dioxide
        Gb3=0.0+50.0-Lb_out#mass balance to calculate outlet gas flow rate of ethylene
        Gc3=100.0+0.0-L_out#mass balance to calculate outlet gas flow rate of water
       
        for i in range(20):
            h=self.h
            Dc=self.gas_3(x,y,z,a,b,c)
            L=range(21)
            
            c=c+z-Dc
            L[i]=c
            h=h*(i+1)
            print c
            plt.plot(h,L[i],'ro')#to plot change in concentration of water concentration vs step size
            
        print La_out,Lb_out,L_out,Ga3,Gb3,Gc3
plt.plot()
st1=contactr()
st1.final(50.0,50.0,0.0,35.0,35.0,50.0)
plt.show()
img=mpimg.imread(rush)
        
        
        
        
        