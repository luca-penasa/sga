# Autogenerated with SMOP 
from smop.core import *
# SimilarFold.m

    
@function
def SimilarFold(yp=None,psect=None,alpha=None,pslip=None,*args,**kwargs):
    varargin = SimilarFold.varargin
    nargin = SimilarFold.nargin

    #SimilarFold plots the evolution of a similar fold
    
    #   USE: frames = SimilarFold(yp,psect,alpha,pslip)
    
    #   yp = Datums or vertical coordinates of undeformed, horizontal beds
#   psect = A 1 x 2 vector containing the extent of the section, and the 
#           number of points in each bed
#   alpha = Shear angle. Positive for shear antithetic to the fault and
#           negative for shear synthetic to the fault
#   pslip = A 1 x 2 vector containing the total and incremental slip
#   frames = An array structure containing the frames of the fold evolution
#            You can play the movie again just by typing movie(frames)
    
    #   NOTE: Use positive pslip for a normal fault
    
    #MATLAB script written by Nestor Cardozo for the book Structural 
#Geology Algorithms by Allmendinger, Cardozo, & Fisher, 2011. If you use
#this script, please cite this as "Cardozo in Allmendinger et al. (2011)"
    
    #Extent of section and number of points in each bed
    extent=psect[1]
# SimilarFold.m:22
    npoint=psect[2]
# SimilarFold.m:22
    #Make undeformed beds geometry: This is a grid of points along the beds
    xp=arange(0.0,extent,extent / npoint)
# SimilarFold.m:25
    XP,YP=meshgrid(xp,yp,nargout=2)
# SimilarFold.m:26
    #Slip and number of slip increments
    slip=pslip[1]
# SimilarFold.m:29
    sinc=pslip[2]
# SimilarFold.m:29
    ninc=round(slip / sinc)
# SimilarFold.m:30
    #Prompt the user to select the geometry of the fault. If the current fault
#trajectory is not satisfactory, the user can re-select the input points
    a='n'
# SimilarFold.m:34
    while a == 'n':

        #Plot beds
        for i in arange(1,size(yp,2)).reshape(-1):
            plot(XP[i,:],YP[i,:],'k-')
            hold('on')
        axis('equal')
        axis(cat(0,extent,0,dot(2.0,max(yp))))
        disp('Digitize a listric fault shallowing to the right')
        disp('Left mouse button picks points')
        disp('Right mouse button picks last point')
        fault=matlabarray([])
# SimilarFold.m:47
        n=0
# SimilarFold.m:47
        but=1
# SimilarFold.m:47
        while but == 1:

            n=n + 1
# SimilarFold.m:49
            xi,yi,but=ginput(1,nargout=3)
# SimilarFold.m:50
            plot(xi,yi,'-or','LineWidth',1.5)
            fault[n,1]=xi
# SimilarFold.m:52
            fault[n,2]=yi
# SimilarFold.m:52

        hold('off')
        a=input_('Would you like to keep the current fault? (y/n)  ','s')
# SimilarFold.m:55

    
    #Sort fault points in x
    fault=sortrows(fault,1)
# SimilarFold.m:59
    xf=fault[:,1].T
# SimilarFold.m:60
    yf=fault[:,2].T
# SimilarFold.m:61
    #Find tangent of dip of fault segments: df/dx
    dfx=zeros(1,n)
# SimilarFold.m:64
    for i in arange(1,n - 1).reshape(-1):
        dfx[i]=(yf[i + 1] - yf[i]) / (xf[i + 1] - xf[i])
# SimilarFold.m:66
    
    dfx[n]=dfx[n - 1]
# SimilarFold.m:68
    #From the origin of each bed compute the number of points that are in the
#footwall. These points won't move
    fwid=zeros(size(yp,2))
# SimilarFold.m:72
    #Find y of fault below/above bed points
    yfi=interp1(xf,yf,xp,'linear','extrap')
# SimilarFold.m:74
    for i in arange(1,size(yp,2)).reshape(-1):
        fwid[i]=0
# SimilarFold.m:76
        for j in arange(1,size(xp,2)).reshape(-1):
            if yp[i] < yfi[j]:
                fwid[i]=fwid[i] + 1
# SimilarFold.m:79
    
    #Coordinate transformation matrix between horizontal-vertical coordinate 
#system and coordinate system parallel and perpendicular to shear direction
    a11=cos(alpha)
# SimilarFold.m:86
    a12=- sin(alpha)
# SimilarFold.m:87
    a21=sin(alpha)
# SimilarFold.m:88
    a22=copy(a11)
# SimilarFold.m:89
    #Transform fault and beds to coordinate system parallel and perpendicular
#to shear direction
    xfS=dot(xf,a11) + dot(yf,a12)
# SimilarFold.m:93
    
    XPS=dot(XP,a11) + dot(YP,a12)
# SimilarFold.m:94
    
    YPS=dot(XP,a21) + dot(YP,a22)
# SimilarFold.m:95
    #Compute deformation
#Loop over slip increments
    for i in arange(1,ninc).reshape(-1):
        #Loop over number of beds
        for j in arange(1,size(XPS,1)).reshape(-1):
            #Loop over number of bed points in hanging wall
            for k in arange(fwid[j] + 1,size(XPS,2)).reshape(-1):
                #Find local tangent of fault dip: df/dx
                if XPS[j,k] <= xfS[1]:
                    ldfx=dfx[1]
# SimilarFold.m:106
                else:
                    if XPS[j,k] >= xfS[n]:
                        ldfx=dfx[n]
# SimilarFold.m:108
                    else:
                        a='n'
# SimilarFold.m:110
                        L=1
# SimilarFold.m:110
                        while a == 'n':

                            if XPS[j,k] >= xfS[L] and XPS[j,k] < xfS[L + 1]:
                                ldfx=dfx[L]
# SimilarFold.m:113
                                a='s'
# SimilarFold.m:114
                            else:
                                L=L + 1
# SimilarFold.m:116

                #Compute velocities perpendicular and along shear direction
             #Equations 11.13 and 11.15
                vxS=dot(sinc,a11)
# SimilarFold.m:122
                vyS=(dot(sinc,(dot(a11,a21) + dot(ldfx,a11 ** 2)))) / (a11 - dot(ldfx,a21))
# SimilarFold.m:123
                XPS[j,k]=XPS[j,k] + vxS
# SimilarFold.m:125
                YPS[j,k]=YPS[j,k] + vyS
# SimilarFold.m:126
        #Transform beds back to geographic coordinate system
        XP=dot(XPS,a11) + dot(YPS,a21)
# SimilarFold.m:131
        YP=dot(XPS,a12) + dot(YPS,a22)
# SimilarFold.m:132
        #Fault
        plot(xf,yf,'r-','LineWidth',2)
        hold('on')
        for j in arange(1,size(yp,2)).reshape(-1):
            #Footwall
            plot(XP[j,1:1:fwid[j]],YP[j,1:1:fwid[j]],'k-')
            plot(XP[j,fwid[j] + 1:1:size(XP,2)],YP[j,fwid[j] + 1:1:size(XP,2)],'k-')
        #Plot settings
        text(dot(0.8,extent),dot(1.75,max(yp)),strcat('Slip = ',num2str(dot(i,sinc))))
        axis('equal')
        axis(cat(0,extent,0,dot(2.0,max(yp))))
        hold('off')
        frames[i]=getframe
# SimilarFold.m:152
    
    return frames
    
if __name__ == '__main__':
    pass
    