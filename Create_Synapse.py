# Create_Synapse.py
from brian2 import *
from Resources.Equations import *
from Resources.Parameters import *
import numpy as np
import random
import csv
import os

random.seed(185624)

def Create_Synapse_CN(MR_SA, MR_RA, MR_PC, PN_SA, PN_RA, PN_PC):
    """Creates synapses between Mechanoreceptors and Cuneate Nucleus."""
    # SA to PN
    MR_SA_to_PN_SA = Synapses(MR_SA, PN_SA, 'w:volt', on_pre='v += w', method='euler', delay=Delay * ms)
    MR_SA_to_PN_SA.connect(condition='(x_post==x_pre) and (y_post==y_pre)')
    MR_SA_to_PN_SA.w = np.random.uniform(750, 850, len(MR_SA_to_PN_SA)) * mV

    # RA to PN
    MR_RA_to_PN_RA = Synapses(MR_RA, PN_RA, 'w:volt', on_pre='v += w', method='euler', delay=Delay * ms)
    MR_RA_to_PN_RA.connect(condition='(x_post==x_pre) and (y_post==y_pre)')
    MR_RA_to_PN_RA.w = np.random.uniform(550, 650, len(MR_RA_to_PN_RA)) * mV

    # PC to PN
    MR_PC_to_PN_PC = Synapses(MR_PC, PN_PC, 'w:volt', on_pre='v += w', method='euler', delay=Delay * ms)
    MR_PC_to_PN_PC.connect(condition='(x_post==x_pre) and (y_post==y_pre)')
    MR_PC_to_PN_PC.w = np.random.uniform(400, 420, len(MR_PC_to_PN_PC)) * mV

    return MR_SA_to_PN_SA, MR_RA_to_PN_RA, MR_PC_to_PN_PC

def Create_Synapse_CN_To_3b(MR_SA, MR_RA, MR_PC, PN_SA, PN_RA, PN_PC, SA_like, RA_like, PC_like, mixed):
    """Creates synapses between Cuneate Nucleus and Area 3b."""
    # SA to SA_like
    PN_SA_to_SA_like = Synapses(PN_SA, SA_like, 'w:volt', on_pre='v += w', method='euler', delay=Delay * ms)
    for ii in range(N_CN_SA):
        PN_SA_to_SA_like.connect(i=ii, j=[i for i in range(N_3b_SA)], p=0.4)
    PN_SA_to_SA_like.w = np.random.uniform(17, 20, len(PN_SA_to_SA_like)) * mV

    # RA to RA_like
    PN_RA_to_RA_like = Synapses(PN_RA, RA_like, 'w:volt', on_pre='v += w', method='euler', delay=Delay * ms)
    for ii in range(N_CN_RA):
        PN_RA_to_RA_like.connect(i=ii, j=[i for i in range(N_3b_RA)], p=0.4)
    PN_RA_to_RA_like.w = np.random.uniform(17, 21, len(PN_RA_to_RA_like)) * mV

    # PC to PC_like
    PN_PC_to_PC_like = Synapses(PN_PC, PC_like, 'w:volt', on_pre='v += w', method='euler', delay=Delay * ms)
    for ii in range(N_CN_PC):
        PN_PC_to_PC_like.connect(i=ii, j=[i for i in range(N_3b_PC)], p=0.4)
    PN_PC_to_PC_like.w = np.random.uniform(17, 21, len(PN_PC_to_PC_like)) * mV

    # Inputs to Mixed
    PN_SA_to_mixed = Synapses(PN_SA, mixed, 'w:volt', on_pre='v += w', method='euler', delay=Delay * ms)
    for ii in range(N_CN_SA): PN_SA_to_mixed.connect(i=ii, j=[i for i in range(N_3b_mixed)], p=0.05)
    PN_SA_to_mixed.w = np.random.uniform(15, 20, len(PN_SA_to_mixed)) * mV

    PN_RA_to_mixed = Synapses(PN_RA, mixed, 'w:volt', on_pre='v += w', method='euler', delay=Delay * ms)
    for ii in range(N_CN_RA): PN_RA_to_mixed.connect(i=ii, j=[i for i in range(N_3b_mixed)], p=0.05)
    PN_RA_to_mixed.w = np.random.uniform(18, 25, len(PN_RA_to_mixed)) * mV

    PN_PC_to_mixed = Synapses(PN_PC, mixed, 'w:volt', on_pre='v += w', method='euler', delay=Delay * ms)
    for ii in range(N_CN_PC): PN_PC_to_mixed.connect(i=ii, j=[i for i in range(N_3b_mixed)], p=0.05)
    PN_PC_to_mixed.w = np.random.uniform(18, 25, len(PN_PC_to_mixed)) * mV

    return PN_SA_to_SA_like, PN_RA_to_RA_like, PN_PC_to_PC_like, PN_SA_to_mixed, PN_RA_to_mixed, PN_PC_to_mixed

def Create_Synapse_IN(MR_SA, MR_RA, MR_PC, PN_SA, PN_RA, PN_PC, SA_like, RA_like, PC_like, mixed, IN_CN_SA, IN_CN_RA, IN_CN_PC, IN_SA_like, IN_RA_like, IN_PC_like, IN_mixed):
    """Creates inhibitory synapses and feedforward inhibitory loops."""
    
    # Helper function to apply inhibitory lateral connections
    def connect_lateral(syn_obj, weight_val):
        conditions = [
            '(x_post==x_pre) and (y_post==y_pre+1)', '(x_post==x_pre) and (y_post==y_pre-1)',
            '(x_post==x_pre+1) and (y_post==y_pre)', '(x_post==x_pre+1) and (y_post==y_pre+1)',
            '(x_post==x_pre+1) and (y_post==y_pre-1)', '(x_post==x_pre-1) and (y_post==y_pre)',
            '(x_post==x_pre-1) and (y_post==y_pre-1)', '(x_post==x_pre-1) and (y_post==y_pre+1)'
        ]
        for cond in conditions:
            syn_obj.connect(condition=cond)
        syn_obj.w = np.random.uniform(weight_val, weight_val, len(syn_obj)) * mV

    # MR to IN_CN
    MR_SA_to_IN_CN_SA = Synapses(MR_SA, IN_CN_SA, 'w:volt', on_pre='v += w', method='euler', delay=Delay*ms)
    MR_SA_to_IN_CN_SA.connect(condition='(x_post==x_pre) and (y_post==y_pre)')
    MR_SA_to_IN_CN_SA.w = np.random.uniform(1950, 2000, len(MR_SA_to_IN_CN_SA)) * mV

    MR_RA_to_IN_CN_RA = Synapses(MR_RA, IN_CN_RA, 'w:volt', on_pre='v += w', method='euler', delay=Delay*ms)
    MR_RA_to_IN_CN_RA.connect(condition='(x_post==x_pre) and (y_post==y_pre)')
    MR_RA_to_IN_CN_RA.w = np.random.uniform(400, 420, len(MR_RA_to_IN_CN_RA)) * mV

    MR_PC_to_IN_CN_PC = Synapses(MR_PC, IN_CN_PC, 'w:volt', on_pre='v += w', method='euler', delay=Delay*ms)
    MR_PC_to_IN_CN_PC.connect(condition='(x_post==x_pre) and (y_post==y_pre)')
    MR_PC_to_IN_CN_PC.w = np.random.uniform(500, 550, len(MR_PC_to_IN_CN_PC)) * mV

    # PN to IN (Area 3b)
    PN_SA_to_IN_SA_like = Synapses(PN_SA, IN_SA_like, 'w:volt', on_pre='v += w', method='euler', delay=Delay*ms)
    PN_SA_to_IN_SA_like.connect(condition='i==j')
    PN_SA_to_IN_SA_like.w = np.random.uniform(900, 1100, len(PN_SA_to_IN_SA_like)) * mV

    PN_RA_to_IN_RA_like = Synapses(PN_RA, IN_RA_like, 'w:volt', on_pre='v += w', delay=Delay*ms)
    PN_RA_to_IN_RA_like.connect(condition='i==j')
    PN_RA_to_IN_RA_like.w = np.random.uniform(500, 1000, len(PN_RA_to_IN_RA_like)) * mV

    PN_PC_to_IN_PC_like = Synapses(PN_PC, IN_PC_like, 'w:volt', on_pre='v += w', delay=Delay*ms)
    PN_PC_to_IN_PC_like.connect(condition='i==j')
    PN_PC_to_IN_PC_like.w = np.random.uniform(1000, 1000, len(PN_PC_to_IN_PC_like)) * mV

    # PN to IN_mixed
    PN_SA_to_IN_Mixed = Synapses(PN_SA, IN_mixed, 'w:volt', on_pre='v += w', method='euler', delay=Delay*ms)
    for ii in range(N_CN_SA): PN_SA_to_IN_Mixed.connect(i=ii, j=[i for i in range(N_IN_mixed)], p=0.3)
    PN_SA_to_IN_Mixed.w = np.random.uniform(10, 15, len(PN_SA_to_IN_Mixed)) * mV

    PN_RA_to_IN_Mixed = Synapses(PN_RA, IN_mixed, 'w:volt', on_pre='v += w', method='euler', delay=Delay*ms)
    for ii in range(N_CN_RA): PN_RA_to_IN_Mixed.connect(i=ii, j=[i for i in range(N_IN_mixed)], p=0.3)
    PN_RA_to_IN_Mixed.w = np.random.uniform(30, 40, len(PN_RA_to_IN_Mixed)) * mV

    PN_PC_to_IN_Mixed = Synapses(PN_PC, IN_mixed, 'w:volt', on_pre='v += w', method='euler', delay=Delay*ms)
    for ii in range(N_CN_PC): PN_PC_to_IN_Mixed.connect(i=ii, j=[i for i in range(N_IN_mixed)], p=0.3)
    PN_PC_to_IN_Mixed.w = np.random.uniform(30, 40, len(PN_PC_to_IN_Mixed)) * mV

    # Lateral Inhibition
    IN_SA_like_to_SA_like = Synapses(IN_SA_like, SA_like, 'w:volt', on_pre='v -= w', method='euler', delay=Delay*ms)
    connect_lateral(IN_SA_like_to_SA_like, 40)

    IN_RA_like_to_RA_like = Synapses(IN_RA_like, RA_like, 'w:volt', on_pre='v -= w', method='euler', delay=0*ms)
    connect_lateral(IN_RA_like_to_RA_like, 40)

    IN_PC_like_to_PC_like = Synapses(IN_PC_like, PC_like, 'w:volt', on_pre='v -= w', method='euler', delay=0*ms)
    connect_lateral(IN_PC_like_to_PC_like, 40)

    IN_mixed_to_mixed = Synapses(IN_mixed, mixed, 'w:volt', on_pre='v -= w', method='euler', delay=Delay*ms)
    connect_lateral(IN_mixed_to_mixed, 40)

    IN_CN_SA_to_PN_SA = Synapses(IN_CN_SA, PN_SA, 'w:volt', on_pre='v -= w', method='euler', delay=Delay*ms)
    connect_lateral(IN_CN_SA_to_PN_SA, 200)

    IN_CN_RA_to_PN_RA = Synapses(IN_CN_RA, PN_RA, 'w:volt', on_pre='v -= w', method='euler', delay=Delay*ms)
    connect_lateral(IN_CN_RA_to_PN_RA, 200)

    IN_CN_PC_to_PN_PC = Synapses(IN_CN_PC, PN_PC, 'w:volt', on_pre='v -= w', method='euler', delay=Delay*ms)
    connect_lateral(IN_CN_PC_to_PN_PC, 200)

    return (MR_SA_to_IN_CN_SA, MR_RA_to_IN_CN_RA, MR_PC_to_IN_CN_PC, PN_SA_to_IN_SA_like, 
            PN_RA_to_IN_RA_like, PN_PC_to_IN_PC_like, PN_SA_to_IN_Mixed, PN_RA_to_IN_Mixed, 
            PN_PC_to_IN_Mixed, IN_SA_like_to_SA_like, IN_RA_like_to_RA_like, IN_PC_like_to_PC_like, 
            IN_mixed_to_mixed, IN_CN_SA_to_PN_SA, IN_CN_RA_to_PN_RA, IN_CN_PC_to_PN_PC)

def Create_Synapse_SA_res(SA_like, resonate):
    SA_res = Synapses(SA_like, resonate, 'w:1', on_pre='v += w')
    ii = [i for i in range(N_3b_SA) for _ in range(Numb_res)]
    jj = np.arange(N_3b_SA * Numb_res)
    SA_res.connect(i=ii, j=jj)
    SA_res.w = 0.7
    return SA_res

def Create_Synapse_RA_res(RA_like, resonate):
    RA_res = Synapses(RA_like, resonate, 'w:1', on_pre='v += w')
    ii = [i for i in range(N_3b_SA) for _ in range(Numb_res)]
    jj = np.arange(N_3b_SA * Numb_res, N_3b_RA * Numb_res*2)
    RA_res.connect(i=ii, j=jj)
    RA_res.w = 0.7
    return RA_res

def Create_Synapse_PC_res(PC_like, resonate):
    PC_res = Synapses(PC_like, resonate, 'w:1', on_pre='v += w')
    ii = [i for i in range(N_3b_SA) for _ in range(Numb_res)]
    jj = np.arange(N_3b_RA * Numb_res*2, N_3b_PC * Numb_res*3)
    PC_res.connect(i=ii, j=jj)
    PC_res.w = 0.7
    return PC_res

def Create_Synapse_mixed_res(mixed, resonate):
    mixed_res = Synapses(mixed, resonate, 'w:1', on_pre='v += w')
    ii = [i for i in range(N_3b_mixed) for _ in range(Numb_res)]
    jj = np.arange(N_3b_PC * Numb_res*3, (N_3b_mixed * Numb_res + (N_3b_PC * Numb_res*3)))
    mixed_res.connect(i=ii, j=jj)
    mixed_res.w = 0.7
    return mixed_res

def Create_Synapse_Class(resonate, PN_Class, csv_path="./data/unique_neurons.csv"):
    """Connects resonator neurons to output classes based on a CSV mapping."""
    loaded_neurons = {}
    try:
        with open(csv_path, mode="r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                class_name = row[0]
                neuron_indices = list(map(int, row[1].split(",")))
                loaded_neurons[class_name] = neuron_indices
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
        return None, None

    num_classes = 15
    neurons_per_class = 500
    neurons_per_PN_group = 1

    resonate_to_PN = Synapses(resonate, PN_Class, 'w : volt', on_pre='v += w')
    
    for class_idx, (class_name, neuron_indices) in enumerate(loaded_neurons.items()):
        ii = np.array(neuron_indices)
        start_idx = class_idx * neurons_per_PN_group
        end_idx = start_idx + neurons_per_PN_group
        jj = np.arange(start_idx, end_idx)
        resonate_to_PN.connect(i=np.repeat(ii, len(jj)), j=np.tile(jj, len(ii)))
        
    resonate_to_PN.delay = 'int(100*rand())*ms'
    resonate_to_PN.w = '30 * mV'

    Lateral_class = Synapses(PN_Class, PN_Class, 'w:volt', on_pre='v -= w', method='euler', delay=Delay*ms)
    Lateral_class.connect(condition='i!=j')
    Lateral_class.w = 0 * mV

    return resonate_to_PN, Lateral_class
