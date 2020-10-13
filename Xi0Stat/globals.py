import os
dirName = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

miscPath = os.path.join(dirName, 'data', 'misc')



###########################
# CONSTANTS
###########################

clight = 2.99792458* 10**5

l_CMB, b_CMB = (263.99, 48.26)
v_CMB = 369

# Solar magnitude in B and K band
MBSun=5.498
MKSun=3.27

# Cosmologival parameters used in GLADE for z-dL conversion
H0GLADE=70
Om0GLADE=0.27



# Parameters of Schechter function in B band in units of 10^10 solar B band
# for h0=0.7
LBstar07 =2.45
phiBstar07  = 5.5 * 1e-3
alphaB07 =-1.07


# Parameters of Schechter function in K band in units of 10^10 solar K band
# for h0=0.7
LKstar07 = 10.56
phiKstar07 = 3.70 * 1e-3
alphaK07 =-1.02




###########################
###########################

import multiprocessing

nCores = multiprocessing.cpu_count()

def fun(f, q_in, q_out):
    while True:
        i, x = q_in.get()
        if i is None:
            break
        q_out.put((i, f(x)))


def parmap(f, X):
    q_in = multiprocessing.Queue(1)
    q_out = multiprocessing.Queue()

    proc = [multiprocessing.Process(target=fun, args=(f, q_in, q_out))
            for _ in range(nCores)]
    for p in proc:
        p.daemon = True
        p.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(X)]
    [q_in.put((None, None)) for _ in range(nCores)]
    res = [q_out.get() for _ in range(len(sent))]

    [p.join() for p in proc]

    return [x for i, x in sorted(res)]


###########################
###########################

    
def get_SchParams(self, Lstar, phiStar, h0):
        '''
        Input: Hubble parameter h0, values of Lstar, phiStar for h0=0.7
        Output: Schechter function parameters L_*, phi_* rescaled by h0
        '''
        Lstar = Lstar*(h0/0.7)**(-2)
        phiStar = phiStar*(h0/0.7)**(3)
        return Lstar, phiStar



def get_SchNorm(self, phistar, Lstar, alpha, Lcut):
        '''
        
        Input:  - Schechter function parameters L_*, phi_*, alpha
                - Lilit of integration L_cut in units of 10^10 solar lum.
        
        Output: integrated Schechter function up to L_cut in units of 10^10 solar lum.
        '''
        from scipy.special import gammaincc
        from scipy.special import gamma
                
        norm= phistar*Lstar*gamma(alpha+2)*gammaincc(alpha+2, Lcut)
        return norm
