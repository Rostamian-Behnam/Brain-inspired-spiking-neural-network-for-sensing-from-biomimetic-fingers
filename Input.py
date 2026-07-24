# Input.py
from brian2 import *
import numpy as np
import random
from Resources.Parameters import *

np.random.seed(185624)
random.seed(185624)

def simulate(row, column, duration, trials):
    """Simulates pulse input data for specified taxels."""
    sample_per_second = 1000
    sample_per_duration = int(sample_per_second * duration)
    total_samples = sample_per_duration * trials
    time = np.linspace(0, duration * trials, total_samples)

    data_all_trials = []
    for i in range(trials):
        amplitude = 0.5 
        array_3x3 = np.zeros((row, column))
        pulse_duration = 0.03 + 0.1 * (random.randint(0, 10) * 0.001)
        
        pulse1_taxels = [0, 3, 6]
        pulse2_taxels = [1, 4, 7]
        pulse3_taxels = [2, 5, 8]

        data_trial = np.zeros((sample_per_duration, 27))
        for t in range(sample_per_duration):
            array_3x3_flat = array_3x3.flatten()
            if 0 <= time[t] < pulse_duration:
                for taxel in pulse1_taxels: array_3x3_flat[taxel] = amplitude
            elif pulse_duration <= time[t] < 2 * pulse_duration:
                for taxel in pulse2_taxels: array_3x3_flat[taxel] = amplitude
            elif 2 * pulse_duration <= time[t] < 3 * pulse_duration:
                for taxel in pulse3_taxels: array_3x3_flat[taxel] = amplitude
            data_trial[t, :] = np.repeat(array_3x3_flat, 3)
            
        data_all_trials.append(data_trial)

    data = np.concatenate(data_all_trials, axis=0)
    return np.transpose(data), duration * trials, 1000 / sample_per_second, total_samples

def Run_recorded(texture, speed, trials, type_, force, data_dir="./data"):
    """Loads recorded tactile data from a .npy file."""
    file_path = f'{data_dir}/allLNData{speed}mms{force}g_{type_}.npy'
    data1 = np.load(file_path)
    
    combined_data = data1
    window_size = 40
    smooth = np.zeros((18, len(combined_data[texture, 0, :, trials]) - window_size + 1))
    for i in range(18):
        smooth[i, :] = np.convolve(combined_data[texture, i, :, trials], np.ones(window_size) / window_size, mode='valid')
    
    return smooth, 1

def sinusoidal(frequency, duration):
    """Generates a sinusoidal input signal."""
    sample = int(duration * 10)
    time_sine = np.linspace(0, duration, sample)
    A = 0.01
    sine_input = A * np.sin(time_sine * frequency * 2 * np.pi) 
    data = np.zeros((18, sample))
    for i in range(18):
        data[i, :] = sine_input + A
    return data, (time_sine) * 1000, duration / sample, sample
