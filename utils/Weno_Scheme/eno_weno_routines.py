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