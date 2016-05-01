# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:32:51 2016

@author: Omkar Mehta
"""

import numpy as np
import matplotlib.pyplot as plt
import pylab
#create random list
Z=np.random.randint(4,size=(6,6))
z=list(Z)
'''z=[[0,1,2,3,0,1],
   [1,2,3,0,1,2],
   [2,3,0,1,2,3],
   [3,0,1,2,3,0],
   [0,1,2,3,0,1],
   [1,2,3,0,1,2]]'''

def count_neighbors(z):
    shape=len(z),len(z[0])
    zero=[0,0,0,0,0,0,0,0]
    A=[zero,zero,zero,zero,
       zero,zero,zero,zero,
       zero,zero,zero,zero,
       zero,zero,zero,zero]
    for y in range(1,5,1):
        A[y-1]=[z[0][y-1],z[0][y],z[0][y+1],
             z[1][y-1],       z[1][y+1],
             z[2][y-1],z[2][y],z[2][y+1]]  
    for y in range(1,5,1):
        A[y+3]=[z[1][y-1],z[1][y],z[1][y+1],
             z[2][y-1],       z[2][y+1],
             z[3][y-1],z[3][y],z[3][y+1]]  
    for y in range(1,5,1):
        A[y+7]=[z[2][y-1],z[2][y],z[2][y+1],
             z[3][y-1],       z[3][y+1],
             z[4][y-1],z[4][y],z[4][y+1]]  									
    for y in range(1,5,1):
        A[y+11]=[z[3][y-1],z[3][y],z[3][y+1],
             z[4][y-1],       z[4][y+1],
             z[5][y-1],z[5][y],z[5][y+1]]          
    a=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    b=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    c=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    d=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(16):

        a[i]=A[i].count(0)
        b[i]=A[i].count(1)
        c[i]=A[i].count(2)
        d[i]=A[i].count(3)
    return [a,b,c,d]
print(count_neighbors(z))

def iterate(z):
    N=count_neighbors(z)

    for y in range(1,5,1):
            x=1
            if z[x][y]==2 and N[1][y-1]<2:
                z[x][y]=0
            if z[x][y]==0 and N[1][y-1]>=2 and N[2][y-1]>1:
                z[x][y]=2
            if z[x][y]==0 and N[1][y-1]>0:
                z[x][y]=1
            if z[x][y]==1 and N[1][y-1]>2:
                z[x][y]=2
            if z[x][y]==3 and N[2][y-1]<2:
                z[x][y]=0
            if z[x][y]==1 and N[2][y-1]>=2 and N[3][y-1]>1:
                z[x][y]=3
    for y in range(1,5,1):
            x=2
            if z[x][y]==2 and N[1][y+3]<2:
                z[x][y]=0
            if z[x][y]==0 and N[1][y+3]>=2 and N[2][y+3]>1:
                z[x][y]=2
            if z[x][y]==0 and N[1][y+3]>0:
                z[x][y]=1
            if z[x][y]==1 and N[1][y+3]>2:
                z[x][y]=2
            if z[x][y]==3 and N[2][y+3]<2:
                z[x][y]=0
            if z[x][y]==1 and N[2][y+3]>=2 and N[3][y+3]>1:
                z[x][y]=3
    for y in range(1,5,1):
            x=3
            if z[x][y]==2 and N[1][y+7]<2:
                z[x][y]=0
            if z[x][y]==0 and N[1][y+7]>=2 and N[2][y+7]>1:
                z[x][y]=2
            if z[x][y]==0 and N[1][y+7]>0:
                z[x][y]=1
            if z[x][y]==1 and N[1][y+7]>2:
                z[x][y]=2
            if z[x][y]==3 and N[2][y+7]<2:
                z[x][y]=0
            if z[x][y]==1 and N[2][y+7]>=2 and N[3][y+7]>1:
                z[x][y]=3
    for y in range(1,5,1):
            x=4
            if z[x][y]==2 and N[1][y+11]<2:
                z[x][y]=0
            if z[x][y]==0 and (N[1][y+11]>=2 or N[2][y+11]>1):
                z[x][y]=2
            if z[x][y]==0 and N[1][y+11]>0:
                z[x][y]=1
            if z[x][y]==1 and N[1][y+11]>2:
                z[x][y]=2
            if z[x][y]==3 and N[2][y+11]<2:
                z[x][y]=0
            if z[x][y]==1 and N[2][y+11]>=2 and N[3][y+11]>1:
                z[x][y]=3
    return z
plt.title('Game of Life')
ans=iterate(z)
plt.imshow(ans,interpolation='nearest')
plt.colorbar()
for i in range(1000):
    ans=iterate(z)
    print(ans)
    plt.imshow(ans,interpolation='nearest')
    plt.pause(.01)
