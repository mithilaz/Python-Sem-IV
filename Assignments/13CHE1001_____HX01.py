import scipy.optimize as sci
import matplotlib.pyplot as plt
import scipy

class HX:
    mA=1;mB=2;P=10;L=10;U=100;n=10;Tain=400;Tbin=300
    def e(self):
        mA=self.mA;mB=self.mB;P=self.P;L=self.L;U=self.U;n=self.n
        Tain=self.Tain;Tbin=self.Tbin
        def CpA(T):
	      CpA=4000+.1*T+0.01*T**2
	      return CpA
    
    
        def CpB(T):
	      CpB=3000+.2*T+0.05*T**2
	      return CpB
        def derA(Ta,Tb):
            derA=	-(P*U*(Ta-Tb))/(mA*CpA(Ta))
            return derA
        def derB(Ta,Tb):
            derB=-(P*U*(Ta-Tb))/(mB*CpB(Tb))
        def B(Tbout):
            Ta0=Tain; Tb0=Tbout
            dx=L/float(n-1)
            Ta1=Ta0+derA(Ta0,Tb0)*dx; Tb1=Tb0+derB(Ta0,Tb0)*dx
            Ta2=Ta0+2*derA(Ta1,Tb1)*dx;Tb2=Tb0+2*derB(Ta1,Tb1)*dx
            for i in range(n-5):
                Ta3=Ta1+2*derA(Ta2,Tb2)*dx;Tb3=Tb1+2*derB(Ta2,Tb2)*dx
                Ta4=Ta2+2*derA(Ta3,Tb3)*dx;Tb4=Tb2+2*derB(Ta3,Ta3)*dx
                Ta1=Ta2;Tb1=Tb2;Ta2=Ta3;Tb2=Tb3;Ta3=Ta4;Tb3=Tb4 
            Ta5=Ta4+derA(Ta4,Tb4)*dx;Tb5=Tb4+derB(Ta4,Tb4)*dx
                																
            return Tb5-Tbin
        Tbout=sci.fsolve(B,327)
        
        Ta0=Tain; Tb0=Tbout
        dx=L/float(n-1)
        Ta1=Ta0+derA(Ta0,Tb0)*dx; Tb1=Tb0+derB(Ta0,Tb0)*dx
        Ta2=Ta0+2*derA(Ta1,Tb1)*dx;Tb2=Tb0+2*derB(Ta1,Tb1)*dx
        for i in range(n-5):
            Ta3=Ta1+2*derA(Ta2,Tb2)*dx;Tb3=Tb1+2*derB(Ta2,Tb2)*dx
            Ta4=Ta2+2*derA(Ta3,Tb3)*dx;Tb4=Tb2+2*derB(Ta3,Ta3)*dx
            Ta1=Ta2;Tb1=Tb2;Ta2=Ta3;Tb2=Tb3;Ta3=Ta4;Tb3=Tb4 
        Ta5=Ta4+derA(Ta4,Tb4)*dx;Tb5=Tb4+derB(Ta4,Tb4)*dx
        deltaHa = mA*(4000*(Ta0-Ta5)+0.1/2*(Ta0**2-Ta5**2)+0.01/3*(Ta0**3-Ta5**3))
        deltaHb= mB*(3000*(Tb0-Tb5)+0.2/2*(Tb0**2-Tb5**2)+0.05/3*(Tb0**3-Tb5**3))
        
        e= scipy.absolute((deltaHa-deltaHb)/deltaHa*100)
        				
        
        return e	

				