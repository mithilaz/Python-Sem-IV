import scipy.optimize as scip
import matplotlib.pyplot as plt
import scipy

class HX:
    mA=1;mB=2;P=10;L=10;U=100;n=10;Tain=400;Tbin=300
    def e(self):
        mA=self.mA;mB=self.mB;P=self.P;L=self.L;U=self.U;n=self.n
        Tain=self.Tain;Tbin=self.Tbin
        
        def B(Tbout):
            Ta0=Tain; Tb0=Tbout
            Cpa0=4000+.1*Ta0+.01*Ta0**2; Cpb0=3000+.2*Tb0+5*.01*Tb0*Tb0
            derA0=-(P*U*(Ta0-Tb0))/(mA*Cpa0);derB0=-(P*U*(Ta0-Tb0))/(mB*Cpb0)
            dx=L/float(n-1)
            Ta1=Ta0+derA0*dx;Tb1=Tb0+derB0*dx
            Cpa1=4000+.1*Ta1+.01*Ta1**2; Cpb1=3000+.2*Tb1+5*.01*Tb1*Tb1
            derA1=-(P*U*(Ta1-Tb1))/(mA*Cpa1);derB1=-(P*U*(Ta1-Tb1))/(mB*Cpb1)
            Ta2=Ta0+2*derA1*dx;Tb2=Tb0+2*derB1*dx
            for i in range(n-5):
                Cpa2=4000+.1*Ta2+.01*Ta2**2; Cpb2=3000+.2*Tb2+5*.01*Tb2*Tb2
                derA2=-(P*U*(Ta2-Tb2))/(mA*Cpa2);derB2=-(P*U*(Ta2-Tb2))/(mB*Cpb2)
                Ta3=Ta1+2*derA2*dx;Tb3=Tb1+2*derB2*dx
                Cpa3=4000+.1*Ta3+.01*Ta3**2; Cpb3=3000+.2*Tb3+5*.01*Tb3*Tb3
                derA3=-(P*U*(Ta3-Tb3))/(mA*Cpa3);derB3=-(P*U*(Ta3-Tb3))/(mB*Cpb3)
                Ta4=Ta2+2*derA3*dx;Tb4=Tb2+2*derB3*dx
                
                Ta1=Ta2;Tb1=Tb2;Ta2=Ta3;Tb2=Tb3;Ta3=Ta4;Tb3=Tb4 
            Cpa4=4000+.1*Ta4+.01*Ta4**2; Cpb4=3000+.2*Tb4+5*.01*Tb4*Tb4
            derA4=-(P*U*(Ta4-Tb4))/(mA*Cpa4);derB4=-(P*U*(Ta4-Tb4))/(mB*Cpb4)
            Ta5=Ta4+derA4*dx;Tb5=Tb4+derB4*dx
            return Tb5-300
        Tbout=scip.fsolve(B,327)
        
        Ta0=Tain; Tb0=Tbout
        Cpa0=4000+.1*Ta0+.01*Ta0**2; Cpb0=3000+.2*Tb0+5*.01*Tb0*Tb0
        derA0=-(P*U*(Ta0-Tb0))/(mA*Cpa0);derB0=-(P*U*(Ta0-Tb0))/(mB*Cpb0)
        dx=L/float(n-1)
        Ta1=Ta0+derA0*dx;Tb1=Tb0+derB0*dx
        Cpa1=4000+.1*Ta1+.01*Ta1**2; Cpb1=3000+.2*Tb1+5*.01*Tb1*Tb1
        derA1=-(P*U*(Ta1-Tb1))/(mA*Cpa1);derB1=-(P*U*(Ta1-Tb1))/(mB*Cpb1)
        Ta2=Ta0+2*derA1*dx;Tb2=Tb0+2*derB1*dx
        for i in range(n-5):
            Cpa2=4000+.1*Ta2+.01*Ta2**2; Cpb2=3000+.2*Tb2+5*.01*Tb2*Tb2
            derA2=-(P*U*(Ta2-Tb2))/(mA*Cpa2);derB2=-(P*U*(Ta2-Tb2))/(mB*Cpb2)
            Ta3=Ta1+2*derA2*dx;Tb3=Tb1+2*derB2*dx
            Cpa3=4000+.1*Ta3+.01*Ta3**2; Cpb3=3000+.2*Tb3+5*.01*Tb3*Tb3
            derA3=-(P*U*(Ta3-Tb3))/(mA*Cpa3);derB3=-(P*U*(Ta3-Tb3))/(mB*Cpb3)
            Ta4=Ta2+2*derA3*dx;Tb4=Tb2+2*derB3*dx
                
            Ta1=Ta2;Tb1=Tb2;Ta2=Ta3;Tb2=Tb3;Ta3=Ta4;Tb3=Tb4 
        Cpa4=4000+.1*Ta4+.01*Ta4**2; Cpb4=3000+.2*Tb4+5*.01*Tb4*Tb4
        derA4=-(P*U*(Ta4-Tb4))/(mA*Cpa4);derB4=-(P*U*(Ta4-Tb4))/(mB*Cpb4)
        Ta5=Ta4+derA4*dx;Tb5=Tb4+derB4*dx 								
        HA = mA*(4000*(Ta0-Ta5)+0.1/2*(Ta0**2-Ta5**2)+0.01/3*(Ta0**3-Ta5**3))
        HB= mB*(3000*(Tb0-Tb5)+0.2/2*(Tb0**2-Tb5**2)+0.05/3*(Tb0**3-Tb5**3))
        
        e= scipy.absolute((HA-HB)/HA*100)
        return e								