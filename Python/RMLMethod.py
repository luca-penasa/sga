# Autogenerated with SMOP 
from smop.core import *
# RMLMethod.m

    
@function
def RMLMethod(xp=None,yp=None,tparams=None,sinc=None,maxit=None,N=None,sigma=None,corrl=None,*args,**kwargs):
    varargin = RMLMethod.varargin
    nargin = RMLMethod.nargin

    #RMLMethod runs a Monte Carlo type, trishear inversion analysis for a 
#folded bed
    
    #   USE: [xbest,fval] = RMLMethod(xp,yp,tparams,sinc,maxit,N,sigma,corrl)
    
    #   xp = column vector with x locations of points along bed
#   yp = column vector with y locations of points along bed  
#   tparams = A vector of guess trishear parameters as in function
#            InvTrishear
#   sinc = slip increment
#   maxit = maximum number of iterations in the optimized search
#   N = number of realizations
#   sigma = Variance
#   corrl = Correlation length
#   xbest = Best-fit models for realizations
#   fval = Objective function values of best-fit models
    
    #   NOTE: Input ramp and trishear angles should be in radians
    
    #   RMLMethod uses function BedRealizations and InvTrishear
    
    #MATLAB script written by Nestor Cardozo for the book Structural 
#Geology Algorithms by Allmendinger, Cardozo, & Fisher, 2011. If you use
#this script, please cite this as "Cardozo in Allmendinger et al. (2011)"
    
    #Generate realizations
    rlzt=BedRealizations(xp,yp,N,sigma,corrl)
# RMLMethod.m:28
    #Initialize xbesti and fvali
    xbesti=zeros(N + 1,4)
# RMLMethod.m:31
    fvali=zeros(N + 1,1)
# RMLMethod.m:32
    #Find best-fit model for each realization
    count=1
# RMLMethod.m:35
    for i in arange(1,N + 1).reshape(-1):
        xbest,fval,flag=InvTrishear(rlzt[:,1,i],rlzt[:,2,i],tparams,sinc,maxit,nargout=3)
# RMLMethod.m:37
        if flag > 0:
            xbesti[count,:]=xbest
# RMLMethod.m:41
            fvali[count,:]=fval
# RMLMethod.m:42
            disp(cat('Realization ',num2str(i),'  fval = ',num2str(fval)))
            count=count + 1
# RMLMethod.m:46
    
    #Remove not used elements of xbesti and fvali
    xbesti[count:N + 1,:]=[]
# RMLMethod.m:51
    fvali[count:N + 1,:]=[]
# RMLMethod.m:52
    return xbesti,fvali
    
if __name__ == '__main__':
    pass
    