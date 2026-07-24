# Equations.py
from brian2 import *
from Resources.Parameters import *

# ---------------------------------------------------------
# Mechanoreceptor Equations (SA, RA, PC)
# ---------------------------------------------------------
eqs_SA = '''
    dv/dt = (0.04/ms/mV)*v**2 + (5/ms)*v + 140*mV/ms - u + (D_SA*volt/ms) + 0*sigma*xi*tau*(ms**0.5)/ms/ms : volt (unless refractory)
    du/dt = a*(b*v - u) : volt/second
    D_SA = k_SA * I_SA(t - segment_offset, i) : 1
    k_SA : 1
    x : 1
    y : 1        
    segment_offset : second
    a : 1/second
    b : 1/second
'''

eqs_RA = '''
    dv/dt = (0.04/ms/mV)*v**2 + (5/ms)*v + 140*mV/ms - u + (D_RA*volt/ms) + 0*sigma*xi*tau*(ms**0.5)/ms/ms : volt (unless refractory)
    du/dt = 0.7*a*(b*v - u) : volt/second
    D_RA = k_RA * (abs(I_RA(t - segment_offset, i))) : 1
    k_RA : 1
    x : 1
    y : 1  
    segment_offset : second
    a : 1/second
    b : 1/second
'''

eqs_PC = '''
    dv/dt = (0.04/ms/mV)*v**2 + (5/ms)*v + 140*mV/ms - u + (D_PC*mV/ms) + 0*sigma*xi*tau*(ms**0.5)/ms/ms : volt (unless refractory)
    du/dt = 1*a*(b*v - u) : volt/second
    D_PC = k_PC * I_PC(t - segment_offset, i) : 1
    k_PC : 1
    x : 1
    y : 1      
    segment_offset : second
    a : 1/second
    b : 1/second
'''

# ---------------------------------------------------------
# Cuneate Nucleus & Area 3b Equations (PN & IN)
# ---------------------------------------------------------
eqs_PN = '''   
    dv/dt = (0.04/ms/mV)*v**2 + (5/ms)*v + 140*mV/ms - u + 300*Ig/second + 200*Ia/second : volt (unless refractory)
    du/dt = a*(b*v - u) : volt/second
    dIg/dt = (-Ig + Ig1)/taugd : volt
    dIa/dt = (-Ia + Ia1)/tauad : volt
    dIg1/dt = -Ig1/taugr : volt
    dIa1/dt = -Ia1/tauar : volt
    x : 1
    y : 1
    a : 1/second
    b : 1/second
'''        

eqs_IN = '''   
    dv/dt = (0.04/ms/mV)*v**2 + (5/ms)*v + 140*mV/ms - u + 300*Ig/second + 200*Ia/second : volt (unless refractory)
    du/dt = a*(b*v - u) : volt/second
    dIg/dt = (-Ig + Ig1)/taugd : volt
    dIa/dt = (-Ia + Ia1)/(tauad) : volt
    dIg1/dt = -Ig1/taugr : volt
    dIa1/dt = -Ia1/(tauar) : volt
    x : 1
    y : 1    
    a : 1/second
    b : 1/second
'''               

# ---------------------------------------------------------
# Resonator & Gamma Equations
# ---------------------------------------------------------
eqs_RS = '''
    dv/dt = damping*v/second - W*u/second : 1
    du/dt = W*v/second + damping*u/second : 1
'''

threshold = '(v) > vth_RS'
reset = '''
v = 0
u = 0
'''

eqs_ms = '''
    dv/dt = (0.04/ms/mV)*v**2 + (5/ms)*v + 140*mV/ms - u + K_Prim*Rate_Prim + K_Sec*Rate_Sec : volt (unless refractory)
    du/dt = a*(b*v - u) : volt/second
    dFStat/dt = (exp(-1.0/tau_Stat)-1)*FStat/ms + r_Stat/ms*(1/second-FStat)*UU_Stat : 1/second
    dUU_Stat/dt = -UU_Stat/0.3/ms : 1
    ss : volt/second
    dFDyn/dt = (exp(-1.0/tau_Dyn)-1)*FDyn/ms + r_Dyn/ms*(1/second-FDyn)*UU_Dyn : 1/second
    dUU_Dyn/dt = -UU_Dyn/0.3/ms : 1
    BETA_bag1 = B0_bag1 + (Beta1 * FDyn) : 1/second
    BETA_bag2 = B0_bag2 + (Beta2_bag2*FStat) : 1/second
    BETA_chain = B0_chain + (Beta2_chain*FStat) : 1/second
    GAMA_bag1 = Gama1 * FStat : 1/second
    GAMA_bag2 = Gama2_bag2 * FDyn : 1/second
    GAMA_chain = Gama2_chain * FDyn : 1/second
    Sur_Ten1 = Ten_bag1 - K_PR*(L(t,i)-L_SR_0-(Ten_bag1/K_SR)-L_PR_0) - GAMA_bag1*candle*second : candle
    Makh_Ten1 = (BETA_bag1 * CL * (L(t,i)-L_SR_0-(Ten_bag1/K_SR)-R)) * int(DL(t,i)>=0*candle/second) + (BETA_bag1 * CS * (L(t,i)-L_SR_0-(Ten_bag1/K_SR)-R)) * int(DL(t,i)<0*candle/second) : second
    Kasr_Ten1 = Sur_Ten1/Makh_Ten1 : candle/second
    dTen_bag1/dt = DL(t,i) - (sign(Kasr_Ten1)*((abs(Kasr_Ten1*second/candle))**A_MS)*K_SR/second) : candle
    Sur_Ten2 = Ten_bag2 - K_PR*(L(t,i)-L_SR_0-(Ten_bag2/K_SR)-L_PR_0) - GAMA_bag2*candle*second : candle
    Makh_Ten2 = (BETA_bag2 * CL * (L(t,i)-L_SR_0-(Ten_bag2/K_SR)-R)) * int(DL(t,i)>=0*candle/second) + (BETA_bag2 * CS * (L(t,i)-L_SR_0-(Ten_bag2/K_SR)-R)) * int(DL(t,i)<0*candle/second) : second
    Kasr_Ten2 = Sur_Ten2/Makh_Ten2 : candle/second
    dTen_bag2/dt = DL(t,i) - (sign(Kasr_Ten2)*((abs(Kasr_Ten2*second/candle))**A_MS)*K_SR/second) : candle
    Sur_Ten_chain = Ten_chain - K_PR*(L(t,i)-L_SR_0-(Ten_chain/K_SR)-L_PR_0) - GAMA_chain*candle*second : candle
    Makh_Ten_chain = (BETA_chain * CL * (L(t,i)-L_SR_0-(Ten_chain/K_SR)-R)) * int(DL(t,i)>=0*candle/second) + (BETA_chain * CS * (L(t,i)-L_SR_0-(Ten_chain/K_SR)-R)) * int(DL(t,i)<0*candle/second) : second
    Kasr_Ten_chain = Sur_Ten_chain/Makh_Ten_chain : candle/second
    dTen_chain/dt = DL(t,i) - (sign(Kasr_Ten_chain)*((abs(Kasr_Ten_chain*second/candle))**A_MS)*K_SR/second) : candle
    Rate_bag1 = G_bag1 * ((Ten_bag1/K_SR)-(L_SR_N-L_SR_0)) : 1
    Rate_bag2 = G_bag2 * ( (X_SR*(L_SEC_bag2/L_SR_0)*((Ten_bag2/K_SR)-(L_SR_N-L_SR_0)))+((1-X_SR)*(L_SEC_bag2/L_PR_0)*(L(t,i)-(Ten_bag2/K_SR)-L_SR_0-L_PR_N)) ) : 1
    Rate_chain = G_chain *((X_SR*(L_SEC_chain/L_SR_0)*((Ten_chain/K_SR)-(L_SR_N-L_SR_0)))+((1-X_SR)*(L_SEC_chain/L_PR_0)*(L(t,i)-(Ten_chain/K_SR)-L_SR_0-L_PR_N))) : 1
    Rate_Sec = Rate_bag2 + Rate_chain : 1
    Rate_Prim = (Rate_bag1 + S*Rate_Sec)*int(Rate_bag1>Rate_Sec)+(Rate_Sec + S*Rate_bag1)*int(Rate_bag1<Rate_Sec) : 1
    K_Sec : volt/second
    K_Prim : volt/second
    FF = ((abs(Kasr_Ten2*second/candle))**A_MS) :1
'''

reset_eq1 = '''
VT += 8
v = c
u += d
'''

eqs_gamma = '''
    dv/dt = (0.04/ms/mV)*v**2 + (5/ms)*v + 140*mV/ms - u + ss : volt (unless refractory)
    du/dt = a*(b*v - u) : volt/second
    ss : volt/second
'''      

Gama_MS_Syn_eq = '''
    UU_Stat = 1
    UU_Dyn = 1
'''       
            
eqs_resonate = '''
    dv/dt = b_res*v/second - W_res*u/second : 1
    du/dt = W_res*v/second + b_res*u/second : 1
    b_res : 1
    W_res : 1
'''
