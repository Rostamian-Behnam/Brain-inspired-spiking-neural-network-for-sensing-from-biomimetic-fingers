# main.py
# Main execution script for the Tactile Neural Network Simulation

import os
import numpy as np
import random
import matplotlib.pyplot as plt
from brian2 import *

# Import local resources
import Input as FN
from Resources.Create_Neurons import *
from Resources.Create_Synapse import *
from Resources.Monitor import *
from Resources.Parameters import *

# =========================================================
# 1. Initialization & Setup
# =========================================================
np.random.seed(18624)
random.seed(18064)

start_scope()

# Create output directory if it doesn't exist
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

# =========================================================
# 2. Build Network Architecture
# =========================================================
print("Building Network Architecture...")

# Mechanoreceptors
MR_PC, MR_SA, MR_RA, row_SA, row_RA, row_PC, col_SA, col_RA, col_PC = Create_Mechanoreceptors(N_SA, N_RA, N_PC)

# Cuneate Nucleus
(PN_SA, PN_RA, PN_PC, IN_CN_SA, IN_CN_RA, IN_CN_PC, 
 row_PN_SA, row_PN_RA, row_PN_PC, row_IN_CN_SA, row_IN_CN_RA, row_IN_CN_PC, 
 col_PN_SA, col_PN_RA, col_PN_PC, col_IN_CN_SA, col_IN_CN_RA, col_IN_CN_PC) = Create_CN(
    N_CN_SA, N_CN_RA, N_CN_PC, N_in_CN_SA, N_in_CN_RA, N_in_CN_PC, 
    MR_PC, MR_SA, MR_RA, row_SA, row_RA, row_PC, col_SA, col_RA, col_PC)

# Area 3b
SA_like, RA_like, PC_like, mixed, IN_SA_like, IN_RA_like, IN_PC_like, IN_mixed = Create_3b(
    N_3b_SA, N_3b_RA, N_3b_PC, N_in_SA_like, N_in_RA_like, N_in_PC_like, N_IN_mixed, 
    row_PN_SA, row_PN_RA, row_PN_PC, row_IN_CN_SA, row_IN_CN_RA, row_IN_CN_PC, 
    col_PN_SA, col_PN_RA, col_PN_PC, col_IN_CN_SA, col_IN_CN_RA, col_IN_CN_PC)

# Synapses: MR -> CN
MR_SA_to_PN_SA, MR_RA_to_PN_RA, MR_PC_to_PN_PC = Create_Synapse_CN(MR_SA, MR_RA, MR_PC, PN_SA, PN_RA, PN_PC)

# Synapses: CN -> 3b
(PN_SA_to_SA_like, PN_RA_to_RA_like, PN_PC_to_PC_like, 
 PN_SA_to_mixed, PN_RA_to_mixed, PN_PC_to_mixed) = Create_Synapse_CN_To_3b(
    MR_SA, MR_RA, MR_PC, PN_SA, PN_RA, PN_PC, SA_like, RA_like, PC_like, mixed)

# Synapses: Inhibitory loops
(MR_SA_to_IN_CN_SA, MR_RA_to_IN_CN_RA, MR_PC_to_IN_CN_PC, PN_SA_to_IN_SA_like, 
 PN_RA_to_IN_RA_like, PN_PC_to_IN_PC_like, PN_SA_to_IN_Mixed, PN_RA_to_IN_Mixed, 
 PN_PC_to_IN_Mixed, IN_SA_like_to_SA_like, IN_RA_like_to_RA_like, IN_PC_like_to_PC_like, 
 IN_mixed_to_mixed, IN_CN_SA_to_PN_SA, IN_CN_RA_to_PN_RA, IN_CN_PC_to_PN_PC) = Create_Synapse_IN(
    MR_SA, MR_RA, MR_PC, PN_SA, PN_RA, PN_PC, SA_like, RA_like, PC_like, mixed, 
    IN_CN_SA, IN_CN_RA, IN_CN_PC, IN_SA_like, IN_RA_like, IN_PC_like, IN_mixed)

# Monitors
sp_MR_SA, sp_MR_RA, sp_MR_PC = Monitor_MR(MR_SA, MR_RA, MR_PC)
sp_PN_SA, sp_PN_RA, sp_PN_PC, sp_IN_CN_SA, sp_IN_CN_RA, sp_IN_CN_PC = Monitor_CN(PN_SA, PN_RA, PN_PC, IN_CN_SA, IN_CN_RA, IN_CN_PC)
sp_SA_like, sp_RA_like, sp_PC_like, sp_mixed, sp_IN_SA_like, sp_IN_RA_like, sp_IN_PC_like, sp_IN_Mixed = Monitor_3b(
    SA_like, RA_like, PC_like, mixed, IN_SA_like, IN_RA_like, IN_PC_like, IN_mixed)

# Resonators and Classification
resonate = Create_resonate(N_res)
SA_res = Create_Synapse_SA_res(SA_like, resonate)
RA_res = Create_Synapse_RA_res(RA_like, resonate)
PC_res = Create_Synapse_PC_res(PC_like, resonate)
mixed_res = Create_Synapse_mixed_res(mixed, resonate)
Sp_out, _ = Monitor_resonate(resonate)

PN_Class = Create_Class()
resonate_to_PN, Lateral_class = Create_Synapse_Class(resonate, PN_Class)
Sp_PN_Class = Monitor_Class(PN_Class)

# =========================================================
# 3. Data Processing & Simulation Loop
# =========================================================
net = Network(collect())
net.store()  # Store initial state

def process_and_save_file(texture_type, speed, force, output_dir):
    print(f"Processing File: Type={texture_type}, Speed={speed}, Force={force}")
    
    for texture in [3]:
        for trials in [5]:
            print(f"  Processing: Texture {texture}, Trial {trials}")
            
            output_file = f"{output_dir}/count_3b_res_Texture{texture}_trial{trials}_speed{speed}_{texture_type}_{force}.csv"
            if os.path.exists(output_file):
                print(f"    Skipping (file already exists): {output_file}")
                continue
            
            # Generate Data input
            smooth, dt = FN.Run_recorded(texture, speed, trials, texture_type, force)
            total_samples = len(np.transpose(smooth))
            
            # Calculate differentials for RA and PC inputs
            Data_SA = smooth + 0.0
            Data_RA = 1000 * np.abs(np.diff(smooth) / np.diff(np.linspace(0, total_samples, total_samples)))
            Data_PC = 1000 * np.abs(np.diff(Data_RA) / np.diff(np.linspace(0, total_samples, total_samples - 1)))
            
            # Initialize TimedArray inputs
            I_SA = TimedArray(np.transpose(Data_SA), dt * ms)
            I_RA = TimedArray(np.transpose(Data_RA), dt * ms)
            I_PC = TimedArray(np.transpose(Data_PC), dt * ms)
            time_run = len(Data_SA[0, :])
            
            # Restore network state and run
            net.restore()
            print(f"    Running simulation for {time_run} ms...")
            net.run(time_run * ms, report='text')

            # Extract firing rates
            firingRate_res = Sp_out.count
            firingRate_SA_like = sp_SA_like.count
            firingRate_RA_like = sp_RA_like.count
            firingRate_PC_like = sp_PC_like.count
            firingRate_Mixed = sp_mixed.count

            # Save results (uncomment to save)
            # np.savetxt(output_file, firingRate_res, delimiter=',')

# Run the processing loop
speeds = [120]
forces = [500]
types = ['wave']

for type_ in types:
    for speed in speeds:
        for force in forces:
            process_and_save_file(type_, speed, force, output_dir)

# =========================================================
# 4. Visualization (Optional)
# =========================================================
plt.figure(figsize=(10, 4))
plt.plot(Sp_PN_Class.t / ms, Sp_PN_Class.i, '|k', markersize=3)
plt.title('PN_Class Spikes')
plt.xlabel('Time (ms)')
plt.ylabel('Neuron Index')
plt.tight_layout()
plt.show()
