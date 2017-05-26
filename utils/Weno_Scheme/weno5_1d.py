import numpy as np

def ENOweights(k,r):
    #Purpose: compute weights c_rk in ENO expansion 
    # v_[i+1/2] = \sum_[j=0]^[k-1] c_[rj] v_[i-r+j]
    #where k = order and r = shift 

    c = np.zeros(k)

    for j in range(0,k):
            de3 = 0.
            for m in range(j+1,k+1):
                #compute denominator 
                de2 = 0.
                for l in range(0,k+1):
                    #print 'de2:',de2
                    if l is not m:
                        de1 = 1.
                        for q in range(0,k+1):
                            #print 'de1:',de1
                            if (q is not m) and (q is not l):
                                de1 = de1*(r-q+1)


                        de2 = de2 + de1


                #compute numerator 
                de1 = 1.
                for l in range(0,k+1):
                    if (l is not m):
                        de1 = de1*(m-l)

                de3 = de3 + de2/de1


            c[j] = de3


    return c

def nddp(X,Y):
    #Newton's divided difference table 
    #the input are two vectors X and Y that represent points 

    n = len(X)

    DD = np.zeros((n,n+1))

    #inserting x into 1st column of DD-table 
    DD[:,0]=X

    #inserting y into 2nd column of DD-table
    DD[:,1]=Y

    #creates divided difference coefficients 
    #e.g: D[0,0] = (Y[1]-Y[0])/(X[1]-X[0])

    for j in range(0,n-1):
        for k in range(0,n-j-1): #j goes from 0 to n-2
            DD[k,j+2]= (DD[k+1,j+1]-DD[k,j+1])/(DD[k+j+1,0]-DD[k,0])

    return DD

def ENO(xloc, uloc, k):
    #Purpose: compute the left and right cell interface values using an ENO 
    #Approach based on 2k-1 long vectors uloc with cell k 

    #treat special case of k=1 - no stencil to select 
    if (k==1):
        ul = uloc[0]
        ur = uloc[0]

    #Apply ENO procedure 
    S = np.zeros(k,dtype=int)
    S[0] = k
    for kk in range (0,k-1):
        #print 'S:',S
        #left stencil
        xvec = np.zeros(k)
        uvec = np.zeros(k)
        Sindxl = append(S[0]-1, S[0:kk+1])-1
        xvec = xloc[Sindxl]
        uvec = uloc[Sindxl]
        DDl = nddp(xvec,uvec)
        Vl = abs(DDl[0,kk+2])

        #right stencil 
        xvec = np.zeros(k)
        uvec = np.zeros(k)
        Sindxr = append(S[0:kk+1], S[kk]+1)-1
        xvec = xloc[Sindxr]
        uvec = uloc[Sindxr]
        DDr = nddp(xvec,uvec)
        Vr = abs(DDr[0,kk+2])

        #choose stencil through divided differences 
        if (Vr>Vl):
            #print 'Vr>Vl'
            S[0:kk+2] = Sindxl+1
        else:
            S[0:kk+2] = Sindxr+1

    #Compute stencil shift 'r'
    r = k - S[0]

    #Compute weights for stencil 
    cr = ENOweights(k,r)
    cl = ENOweights(k,r-1)

    #Compute cell interface values 
    ur = 0 
    ul = 0 
    for i in range(0,k):
        ur = ur + cr[i]*uloc[S[i]-1]
        ul = ul + cl[i]*uloc[S[i]-1]

    return (ul,ur)

def WENO(xloc, uloc, k):
    #Purpose: compute the left and right cell interface values using ENO 
    #approach based on 2k-1 long vectors uloc with cell k 

    #treat special case of k = 1 no stencil to select 
    if (k==1):
        ul = uloc[0]
        ur = uloc[1]

    #Apply WENO procedure 
    alphal = np.zeros(k)
    alphar = np.zeros(k)
    omegal = np.zeros(k)
    omegar = np.zeros(k)
    beta = np.zeros(k)
    d = np.zeros(k)
    vareps= 1e-6

    #Compute k values of xl and xr based on different stencils 
    ulr = np.zeros(k)
    urr = np.zeros(k)

    for r in  range(0,k):
        cr = ENOweights(k,r)
        cl = ENOweights(k,r-1)

        for i in range(0,k):
            urr[r] = urr[r] + cr[i]*uloc[k-r+i-1] 
            ulr[r] = ulr[r] + cl[i]*uloc[k-r+i-1] 


    #setup WENO coefficients for different orders -2k-1
    if (k==2):
        d[0]=2/3.
        d[1]=1/3.
        beta[0] = (uloc[2]-uloc[1])**2
        beta[1] = (uloc[1]-uloc[0])**2


    if(k==3):
        d[0] = 3/10. 
        d[1] = 3/5.
        d[2] = 1/10.
        beta[0] = 13/12.*(uloc[2]-2*uloc[3]+uloc[4])**2 + 1/4.*(3*uloc[2]-4*uloc[3]+uloc[4])**2
        beta[1] = 13/12.*(uloc[1]-2*uloc[2]+uloc[3])**2 + 1/4.*(uloc[1]-uloc[3])**2
        beta[2] = 13/12.*(uloc[0]-2*uloc[1]+uloc[2])**2 + 1/4.*(3*uloc[2]-4*uloc[1]+uloc[0])**2

    #compute alpha parameters
    for r in range(0,k):
        alphar[r] = d[r]/(vareps+beta[r])**2
        alphal[r] = d[k-r-1]/(vareps+beta[r])**2

    #Compute WENO weights parameters
    for r in range(0,k):
        omegal[r] = alphal[r]/alphal.sum()
        omegar[r] = alphar[r]/alphar.sum()

    #Compute cell interface values
    ul = 0 
    ur = 0 
    for r in range(0,k):
        ul = ul + omegal[r]*ulr[r]
        ur = ur + omegar[r]*urr[r]

    return (ul,ur)