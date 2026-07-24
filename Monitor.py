# Monitor.py
from brian2 import *

# Monitors for Mechanoreceptors
def Monitor_MR(MR_SA, MR_RA, MR_PC):
    return SpikeMonitor(MR_SA), SpikeMonitor(MR_RA), SpikeMonitor(MR_PC)

# Monitors for Cuneate Nucleus
def Monitor_CN(PN_SA, PN_RA, PN_PC, IN_CN_SA, IN_CN_RA, IN_CN_PC):
    sp_PN_SA = SpikeMonitor(PN_SA)
    sp_PN_RA = SpikeMonitor(PN_RA)
    sp_PN_PC = SpikeMonitor(PN_PC)
    sp_IN_CN_SA = SpikeMonitor(IN_CN_SA)
    sp_IN_CN_RA = SpikeMonitor(IN_CN_RA)
    sp_IN_CN_PC = SpikeMonitor(IN_CN_PC)
    return sp_PN_SA, sp_PN_RA, sp_PN_PC, sp_IN_CN_SA, sp_IN_CN_RA, sp_IN_CN_PC

# Monitors for Area 3b
def Monitor_3b(SA_like, RA_like, PC_like, mixed, IN_SA_like, IN_RA_like, IN_PC_like, IN_mixed):
    sp_SA_like = SpikeMonitor(SA_like)
    sp_RA_like = SpikeMonitor(RA_like)
    sp_PC_like = SpikeMonitor(PC_like)
    sp_mixed = SpikeMonitor(mixed)
    sp_IN_SA_like = SpikeMonitor(IN_SA_like)
    sp_IN_RA_like = SpikeMonitor(IN_RA_like)
    sp_IN_PC_like = SpikeMonitor(IN_PC_like)
    sp_IN_Mixed = SpikeMonitor(IN_mixed)
    return sp_SA_like, sp_RA_like, sp_PC_like, sp_mixed, sp_IN_SA_like, sp_IN_RA_like, sp_IN_PC_like, sp_IN_Mixed

# Monitors for Resonator
def Monitor_resonate(resonate):
    st_res = StateMonitor(resonate, ['v', 'u'], record=True)
    Sp_out = SpikeMonitor(resonate)
    return Sp_out, st_res

# Monitor for Class
def Monitor_Class(PN_Class):
    return SpikeMonitor(PN_Class)
