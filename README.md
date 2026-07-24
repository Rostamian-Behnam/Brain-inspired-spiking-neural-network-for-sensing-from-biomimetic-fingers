Here is a professional, research-grade `README.md` file tailored for your GitHub repository. You can copy and paste this directly into a file named `README.md` in your root folder.

***

```markdown
# Tactile-SNN: A Spiking Neural Network Model of Tactile Perception

This repository contains the source code for a biologically plausible Spiking Neural Network (SNN) that simulates the human somatosensory pathway. The model processes tactile data (recorded from physical sensors or simulated) and classifies textures by mimicking the neural mechanisms of human touch—from peripheral mechanoreceptors in the skin to cortical processing in Area 3b.

Built using the [Brian2 simulator](https://briansimulator.org/) for spiking neural networks.

## 🧠 Model Architecture

The network implements a multi-layered hierarchical structure based on human neurobiology:

1. **Mechanoreceptors (MR):** Simulates Slowly Adapting (SA), Rapidly Adapting (RA), and Pacinian Corpuscle (PC) receptors using Izhikevich neuron equations. 
   - *Inputs:* SA receives raw tactile indentation, RA receives the first derivative (velocity), and PC receives the second derivative (acceleration) of the signal.
2. **Cuneate Nucleus (CN):** The first relay station in the brainstem. Includes feedforward excitation via Projection Neurons (PN) and feedforward inhibition via Interneurons (IN) to enhance contrast.
3. **Cortical Area 3b:** The primary somatosensory cortex. Features dedicated sub-populations (SA-like, RA-like, PC-like, and Mixed) with realistic lateral inhibition mechanisms to sharpen spatial acuity.
4. **Resonator Layer:** A layer of resonator neurons (using a 2D linear differential equation model) that integrates the output from Area 3b to capture temporal dynamics.
5. **Classification Layer (PN_Class):** Reads the spike rates from the resonator layer to classify the explored texture into distinct categories based on learned neuron mappings.

## ✨ Key Features
- **Biologically Plausible Neurons:** Utilizes Izhikevich neuron models (Regular Spiking, Fast Spiking, Resonators) to balance biological realism with computational efficiency.
- **Lateral Inhibition:** Implemented in both the Cuneate Nucleus and Area 3b to enhance edge contrast and spatial acuity.
- **Dynamic Synaptic Inputs:** Synaptic weights are initialized using randomized uniform distributions to simulate biological variance.
- **Data-Driven:** Capable of processing pre-recorded tactile array data (18-channel) or generating synthetic sinusoidal/pulse inputs.

## 📂 Repository Structure

```text
tactile-snn/
│
├── main.py                  # Main execution script: builds network, runs simulation, plots data
├── Input.py                 # Handles loading recorded .npy data and generating synthetic inputs
├── README.md
├── requirements.txt
│
├── data/                    # Place your input data here (not included in repo)
│   ├── allLNData*.npy       # Pre-recorded tactile sensor data
│   └── unique_neurons.csv   # Mapping of resonator neurons to texture classes
│
├── output/                  # Simulation results are saved here (auto-generated)
│
└── Resources/               # Core neural network definitions
    ├── Parameters.py        # All network, synaptic, and muscular parameters
    ├── Equations.py         # Differential equations for neurons and synapses
    ├── Monitor.py           # Brian2 SpikeMonitor and StateMonitor setups
    ├── Create_Neurons.py    # Functions to instantiate neuron populations
    └── Create_Synapse.py    # Synaptic connection logic and weight initialization
```

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- It is highly recommended to use a virtual environment (e.g., `conda` or `venv`).

### 2. Install Dependencies
Clone the repository and install the required Python packages:
```bash
git clone https://github.com/YOUR_USERNAME/tactile-snn.git
cd tactile-snn
pip install -r requirements.txt
```

### 3. Prepare the Data
Due to file size limits, the raw dataset is not included in this repository. 
1. Create a folder named `data` in the root directory.
2. Place your recorded tactile data `.npy` files inside the `data` folder.
3. Ensure you have a `unique_neurons.csv` file mapping resonator neuron indices to texture classes, and place it in the `data` folder.

## 🚀 Usage

To run the simulation, execute the `main.py` script from the root directory:

```bash
python main.py
```

### Modifying the Simulation
You can easily change the simulation parameters (speed, force, texture type) in the data processing loop inside `main.py`:
```python
# Run the processing loop
speeds = [120]      # Sliding speed (mm/s)
forces = [500]      # Applied force (grams)
types = ['wave']    # Texture types ('wave', 'rect', 'circ')

for type_ in types:
    for speed in speeds:
        for force in forces:
            process_and_save_file(type_, speed, force, output_dir)
```

## 📈 Output
The script will:
1. Print the network building steps and simulation progress to the console.
2. Save spike count CSV files into the `./output/` directory (uncomment the `np.savetxt` lines in `main.py` to enable saving).
3. Display a raster plot of the PN_Class (Classification Layer) spikes upon completion.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Citation
If you use this code in your research, please cite the corresponding paper:
""Brain-inspired spiking neural network for sensing from biomimetic fingers: motion, direction, speed, force, and invariant texture recognition""
