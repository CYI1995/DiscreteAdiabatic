import numpy  as np
import scipy
import math
from scipy import linalg
from matplotlib import pyplot as plt
import random

def proj(vec,dim):
    P = np.zeros((dim,dim),dtype = complex)
    for i in range(dim):
        vi = vec[i]
        for j in range(dim):
            P[i][j] = np.conj(vi)*vec[j]

    return P

def Marzlin_Sanders(s,T):

    theta = math.pi*s

    vx = math.pi*math.cos(2*theta) - math.pi*math.sin(2*theta)*math.sin(2*T*theta)/T 
    vy = math.pi*math.sin(2*theta) + math.pi*math.cos(2*theta)*math.sin(2*T*theta)/T
    vz = 2*math.pi*math.sin(T*theta)**2/T

    return np.array([[vz,vx-1j*vy],[vx+1j*vy,-vz]])

def Marzlin_Sanders_firstderiv(s,T):

    theta = 2*math.pi*s

    vx = -2*math.pi**2*math.sin(theta)*(1 + math.cos(T*theta)) - 2*math.pi**2*math.sin(T*theta)*math.cos(theta)/T
    vy = 2*math.pi**2*math.cos(theta)*(1 + math.cos(T*theta)) - 2*math.pi**2*math.sin(T*theta)*math.sin(theta)/T
    vz = 2*math.pi**2*math.sin(T*theta)

    return np.array([[vz,vx-1j*vy],[vx+1j*vy,-vz]])

# Number of site is 2, dimension is 4
site = 1
dim = 2

# Set the number of total steps to be L = 100
L = 100
# Set total simulation time to be T = 20
T = 1
dt = T/L
# Parameter that determines H''(s)
T0 = 500


H_temp = Marzlin_Sanders(0,T0)

# Set the init_state as the ground state of H1
init_state = np.array([1/math.sqrt(2),-1/math.sqrt(2)])

time_step = np.zeros(L)
fid_err = np.zeros(L)
energy_gap = np.zeros(L)
agp = np.zeros(L)

# Discrete_adb is the state evolved under discrete adiabatic evolution,
# and the initial state is the ground state of H1
Discrete_adb = np.zeros(dim,dtype = complex)
for i in range(dim):
    Discrete_adb[i] = init_state[i]

for count in range(L):
    s = (count+1)/L

    # H_temp represents the adiabatic path H(s)
    H_temp = Marzlin_Sanders(s,T0)
    U_temp = scipy.linalg.expm(-1j*H_temp*dt)

    # Discrete_adb is generated by product of adiabatic walk operator
    Discrete_adb = U_temp.dot(Discrete_adb)

    # Ideal_adb is the ground state of H(s)
    gs_temp = np.zeros(dim,dtype = complex)
    fst_temp = np.zeros(dim,dtype = complex)
    eig,vec = np.linalg.eig(H_temp)
    gs = np.argsort(eig)[0]
    fst = np.argsort(eig)[1]
    for i in range(dim):
        gs_temp[i] = vec[i][gs]
        fst_temp[i] = vec[i][fst]

    # fid_err is the fidelity error (1 - |<v1|v2>|**2)**(1/2)
    # energy_gap is the spectral gap of H(s)
    time_step[count] = s
    fid_err[count] = 1 - abs(np.vdot(Discrete_adb,gs_temp))**2
    energy_gap[count] = eig[fst].real - eig[gs].real
    agp[count] = abs(np.vdot(gs_temp,Marzlin_Sanders_firstderiv(s,T0).dot(fst_temp))/energy_gap[count])

plt.scatter(time_step,energy_gap,label = 'energy gap')
plt.scatter(time_step,agp,label = 'adiabatic gauge potential',marker = '.')
plt.plot(time_step,fid_err,label = 'fidelity error')
# plt.ylim(-0.1,1.1)
plt.legend()
plt.show()
