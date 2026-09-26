# SignalLab

A Python-based digital signal processing toolkit built progressively from fundamental signal-processing concepts to practical DSP experiments.

The project follows a **LeetCode-style learning approach**: each DSP concept is implemented as a small problem/challenge, tested, and then added to the toolkit.

## 🚀 Current Features

### Signal Generation
- Sine wave generation with configurable:
  - Amplitude
  - Frequency
  - Sampling frequency
  - Duration
  - Phase

### Signal Composition
- Addition of two signals
- Handles signals with different sampling rates
- Uses interpolation to align signals before combining them

### Frequency-Domain Analysis
- FFT computation using NumPy
- Frequency-axis generation
- Magnitude-spectrum analysis

### Sampling & Nyquist
- Signal sampling
- Nyquist theorem checking
- Sampling-rate experiments

### Aliasing
- Aliasing detection
- Aliased-frequency calculation
- Experimental verification of aliasing using FFT

### Signal Reconstruction
- Reconstruction of sampled signals using linear interpolation

### Convolution
- Linear convolution using NumPy

### Filtering
- Moving-average FIR filtering

---

## 🧠 Learning Progress

| Challenge | Concept | Status |
|---|---|---|
| 001 | Sine Wave Generation | ✅ |
| 002 | Signal Composition & Interpolation | ✅ |
| 003 | FFT Analysis | ✅ |
| 004 | Sampling & Nyquist Theorem | ✅ |
| 005 | Aliasing Detection | ✅ |
| 006 | Aliased Frequency Calculation | ✅ |
| 007 | FFT Verification of Aliasing | ✅ |
| 008 | Signal Reconstruction | ✅ |
| 009 | Linear Convolution | ✅ |
| 010 | Moving-Average Filter | ✅ |

---

## 🛠️ Technologies

- Python
- NumPy
- Matplotlib
- SciPy
- Pandas

---

## ⚙️ Setup

Clone the repository:

```bash
git clone <repository-url>
cd SignalLab
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python main.py
```

---

## 📁 Project Structure

```text
SignalLab/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/              # Local only, not tracked by Git
```

---

## 🎯 Project Goal

SignalLab is being developed as a progressive DSP learning and experimentation platform.

The long-term goal is to build a reusable Python toolkit covering:

- Signal generation
- Sampling and reconstruction
- Fourier analysis
- Convolution
- FIR and IIR filters
- Frequency response
- Modulation and demodulation
- Noise analysis
- Digital communication experiments
- Time-frequency analysis
- DSP visualization

The project will evolve continuously as new concepts and experiments are implemented.

---

## 📌 Current Focus

The next stage will focus on:

1. Noisy signal generation
2. Moving-average filtering experiments
3. FIR filter design
4. Filter frequency response
5. `scipy.signal.freqz`
6. Low-pass, high-pass, band-pass and band-stop filters

---

## 📚 Learning Philosophy

Instead of treating DSP as only a collection of mathematical formulas, SignalLab focuses on implementing each concept in Python and **verifying the theory experimentally through signals, plots and numerical results.**

> Learn → Implement → Test → Visualize → Expand
