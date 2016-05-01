# -*- coding: utf-8 -*-
# model k i n e t i c p a r ame t e r s
Vmax = 2 . 0 # mol / ( L s )
Km = 0 . 5 # mol / L
# ODE d e f i n i t i o n
de f df ( s , t ) :
d s d t = 􀀀Vmax s / (Km+s )
r e turn d s d t
# s e t u p t ime d i s c r e t i z a t i o n
n = 10 # number o f t ime s t e p s
t = numpy . l i n s p a c e ( 0 , 2 . 0 , n )
d t = t [1]􀀀 t [ 0 ]
# a l l o c a t e s t o r a g e spac e and s e t i n i t i a l c o n d i t i o n s
s o l = numpy . z e r o s ( n )
s o l [ 0 ] = 1 . 0 # i n i t i a l S i n mol / L
f o r i in range ( 1 , n ) :
s o l [ i ] = s o l [ i 􀀀1]+ d t  df ( s o l [ i 􀀀1] , t [ i 􀀀1])
p y l a b . p l o t ( t , s o l )
p y l a b . x l a b e l ( " t ime ( d ime n s i o n l e s s ) " )
p y l a b . y l a b e l ( " c o n c e n t r a t i o n ( d ime n s i o n l e s s ) " )
p y l a b . show ( )"""







Created on Sun May 01 19:34:32 2016

@author: rajivgarg
"""
import numpy
import p y l a b
from s c i p y . i n t e g r a t e import o d e i n t
# model k i n e t i c p a r ame t e r s
Vmax = 2 . 0 # mol / ( L s )
Km = 0 . 5 # mol / L
# ODE d e f i n i t i o n
de f df ( c , t ) :
s = c [ 0 ] # s u b s t r a t e c o n c e n t r a t i o n
p = c [ 1 ] # p r o d u c t c o n c e n t r a t i o n
d s d t = 􀀀Vmax s / (Km+s )
dpdt = Vmax s / (Km+s )
r e turn numpy . a r r a y ( [ dsdt , dpd t ] )
# i n i t i a l c o n d i t i o n
c0 = numpy . a r r a y ( [ 1 . 0 , 0 . 0 ] ) # i n i t i a l S , P i n mol / L
t = numpy . l i n s p a c e ( 0 , 2 . 0 , 1 0 0 )
s o l = o d e i n t ( df , c0 , t )
p y l a b . p l o t ( t , s o l )
p y l a b . x l a b e l ( " t ime ( d ime n s i o n l e s s ) " )
p y l a b . y l a b e l ( " c o n c e n t r a t i o n ( d ime n s i o n l e s s ) " )
p y l a b . show ( )







# y0 ’ = y1 and
# y1 ’ = 4( y􀀀t )
de f d f d t ( y , t ) :
dy0dt = y [ 1 ]
dy1dt = 4 . 0  ( y [0]􀀀 t )
r e turn numpy . a r r a y ( [ dy0dt , dy1dt ] )
de f e x a c t ( t ) :
c o e f f = 0.13786
s o l = c o e f f ( numpy . exp ( 2 . 0  t ) 􀀀 numpy . exp (􀀀2.0 t ) ) + t
r e turn s o l
TOL = 1e􀀀6
t = numpy . l i n s p a c e ( 0 . 0 , 1 . 0 , 1 0 0 )
a l p h a = 0 . 0
b e t a = 2 . 0
gamma0 = 1 . 0
gamma1 = 0 . 0
# f i r s t shot , us e bc f o r y , s e t o t h e r t o 0 . 0
y i n i t 1 = numpy . a r r a y ( [ a lpha , gamma0 ] )
y1 = o d e i n t ( d f d t , y i n i t 1 , t )
# g e t imp ac t p o i n t f o r f i r s t s h o t
# n o t e t h i s g e t s t h e l a s t row , f i r s t column e n t r y
end1 = y1 [ 􀀀1 ,0]





p r int ( " Er r o r wi th s h o t : " , math . f a b s ( be t a􀀀end1 ) )
f o r i in range ( 2 0 ) :
# s e cond shot , s e t bc f o r y t o 0 . 0 , o t h e r u s e s 1 . 0
y i n i t 2 = numpy . a r r a y ( [ a lpha , gamma1 ] )
y2 = o d e i n t ( d f d t , y i n i t 2 , t )
end2 = y2 [ 􀀀1 ,0]
p r int ( " Er r o r wi th s h o t : " , math . f a b s ( be t a􀀀end2 ) )
i f math . f a b s ( be t a􀀀end2 ) < TOL:
break
gamma = gamma1􀀀(( end2􀀀b e t a )  ( gamma1􀀀gamma0 ) / ( end2􀀀end1 ) )
gamma0 = gamma1
gamma1 = gamma
end1 = end2
p y l a b . p l o t ( t , y2 [ : , 0 ] )
p y l a b . p l o t ( t , e x a c t ( t ) )
p y l a b . x l a b e l ( ’ x ’ )
p y l a b . y l a b e l ( ’ y ’ )
p y l a b . show ( )





import win32com.client
import scipy
import matplotlib.pyplot as plt
x1 = win32com.client.gencache.EnsureDispatch("Excel.Application")
wb = x1.Workbooks('ExamProblemData.csv')
sheet = wb.Sheets('ExamProblemData')

def getdata(sheet,Range):
    data=sheet.Range(Range).Value
    data=scipy.array(data)
    data=data.reshape((1,len(data)))[0]
    return data
    
x=getdata(sheet, "D2:D11")
y=getdata(sheet, "E2:E11") 

fig=plt.figure(); ax=fig.add_subplot(111)
ax.plot(x, y, 'ro'); fig.canvas.draw()   



