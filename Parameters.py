# Parameters.py
# Import necessary libraries
import numpy as np
from brian2 import *
import random
from brian2.units.allunits import newton
from brian2.units.allunits import candle

# =========================================================
# 1. Network Topology Parameters
# =========================================================
row = 3
column = 3

N_MR = 18           # Total Mechanoreceptors
N_SA = N_MR         # Slowly Adapting
N_RA = N_MR         # Rapidly Adapting
N_PC = N_MR         # Pacinian Corpuscles
Numb_res = 24       # Resonator multiplier

# Cuneate Nucleus (CN)
N_CN_SA = N_SA
N_CN_RA = N_RA
N_CN_PC = N_PC
N_in_CN_SA = N_SA
N_in_CN_RA = N_RA
N_in_CN_PC = N_PC

# Area 3b
N_3b_SA = N_CN_SA * 2
N_3b_RA = N_CN_RA * 2
N_3b_PC = N_CN_PC * 2
N_3b_mixed = N_3b_SA + N_3b_RA + N_3b_PC
N_in_SA_like = N_CN_SA
N_in_RA_like = N_CN_RA
N_in_PC_like = N_CN_PC
N_IN_mixed = int(N_3b_mixed / 4)
N_res = Numb_res * (N_3b_SA + N_3b_RA + N_3b_PC + N_3b_mixed)

# Other areas
N_RS = 1
N_MS = 2
N_CN_MS = N_MS * 1

# =========================================================
# 2. Neural Parameters (Izhikevich Model)
# =========================================================
# Regular neurons
a = 0.02 / ms
b = 0.2 / ms
c = -65 * mV
d = 8 * mV / ms
vth = 30 * mV

# Noise
sig = 50
sigma = 1 * sig * mV
tau = 0.1 * ms

# Fast Spiking neurons
a_FS = 0.1 / ms
b_FS = 0.2 / ms
c_FS = -65 * mV
d_FS = 2 * mV / ms

# Burst Spiking neurons
a_IB = 0.02 / ms
b_IB = 0.2 / ms
c_IB = -55 * mV
d_IB = 4 * mV / ms

# Resonator Spiking neurons
damping = -3.5  # Real part
W = 95           # Imaginary part
vth_RS = 1.6

# =========================================================
# 3. Synaptic Parameters
# =========================================================
Delay = 0
Refractory = 0
taugd = 1 * 5 * ms
tauad = 1 * 2 * ms
taugr = 1 * 0.25 * ms
tauar = 1 * 0.4 * ms

taum = 10 * ms
taupre = 10 * ms
taupost = taupre
gmax = 500
dApre = 1 * mV
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax

# Generate random indices for Mechanoreceptors
list_index = np.arange(N_MR)
random.shuffle(list_index)
sa_ind = list_index[:N_SA]
ra_ind = list_index[N_SA:]

# =========================================================
# 4. Muscle Spindle Model Parameters
# =========================================================
K_SR = 10.4649 * candle
K_PR = 0.15 * candle
B0_bag1 = 0.0605 / second
B0_bag2 = 0.0822 / second
B0_chain = 0.0822 / second
Beta1 = 0.2592
Beta2_bag2 = -0.0460
Beta2_chain = -0.0690
Gama1 = 0.0289
Gama2_bag2 = 0.0636
Gama2_chain = 0.0954
CL = 1 * second * second
CS = 0.42 * second * second
X_SR = 0.7
L_SR_N = 0.0423
L_PR_N = 0.89
G_bag1 = 20000
G_bag2 = 7250
G_chain = 7250
A_MS = 3.3
R = 0.46
L_SR_0 = 0.04
L_PR_0 = 0.76
L_SEC_bag1 = 0
L_SEC_bag2 = 0.04
L_SEC_chain = 0.04
tau_Filter_bag1 = 0.149
tau_Filter_bag2 = 0.205
freq_bag1 = 60
freq_bag2 = 60
freq_chain = 90
P = 2
tau_Stat = 0.425
tau_Dyn = 0.310
r_Stat = 0.09
r_Dyn = 0.08
S = 0.7

a_MS = 0.02 / ms
b_MS = 0.2 / ms
c_MS = -65 * mV
d_MS = 8 * mV / ms
vth_MS = 30 * mV
sigma_MS = sig * mV
tau_MS = 20 * ms
tauTH_MS = 3000 * ms
