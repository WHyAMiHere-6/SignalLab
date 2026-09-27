import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import (
    freqz,
    firwin,
    butter,
    cont2discrete,
    bilinear
)

# Generation of Sine Wave
def generate_sine(A, f, fs, duration, phase=0):
    t = np.arange(0, duration, 1 / fs)
    x = A * np.sin(2 * np.pi * f * t + phase)
    return t, x

# Composite Signal
def composite_signal(x1, t1, x2, t2):
    if not np.isclose(t1[0], t2[0]) or not np.isclose(t1[-1], t2[-1]):
        raise ValueError("Signals must have the same time interval")
    if np.array_equal(t1, t2):
        return t1, x1 + x2
    if len(t1) > len(t2):
        x2_interp = np.interp(t1, t2, x2)
        return t1, x1 + x2_interp
    else:
        x1_interp = np.interp(t2, t1, x1)
        return t2, x1_interp + x2

# FFT
def compute_fft(x, fs):
    X = np.fft.fft(x)
    f = np.fft.fftfreq(len(x), 1 / fs)
    magnitude = np.abs(X)
    return magnitude, f

# Sampling
def sample_signal(A, f, fs, duration):
    t_org = np.arange(0, duration, 1 / (100 * f))
    x_org = A * np.sin(2 * np.pi * f * t_org)
    ts = np.arange(0, duration, 1 / fs)
    x_samp = A * np.sin(2 * np.pi * f * ts)
    if check_aliasing(f, fs):
        print("Nyquist Theorem Not Satisfied")
    else:
        print("Nyquist Theorem Satisfied")
    return t_org, x_org, ts, x_samp


# Nyquist / Aliasing Check
def check_aliasing(f, fs):
    return 2 * f > fs


# Aliased Frequency
def aliased_frequency(f, fs):
    f_alias = f % fs
    if f_alias > fs / 2:
        f_alias = fs - f_alias
    return f_alias

# Signal Reconstruction / Interpolation
def reconstruct_signal(t_old, x_old, t_new):
    x_new = np.interp(t_new, t_old, x_old)
    return x_new

# Linear Convolution
def linear_convolution(x, h):
    y = np.convolve(x, h, mode="full")
    return y


# Moving Average Filter
def moving_average_filter(x, N):
    if N <= 0:
        raise ValueError("N must be greater than 0")
    h = np.ones(N) / N
    y = np.convolve(x, h, mode="valid")
    return y


# Add Noise
def add_noise(x, noise_level):
    noise = np.random.normal(0, noise_level, len(x))
    x_noisy = x + noise
    return x_noisy

# FIR Filter Frequency Response
def filter_frequency_response(b, fs=None):
    if fs is None:
        w, h = freqz(b)
    else:
        w, h = freqz(b, fs=fs)
    magnitude = np.abs(h)
    phase = np.angle(h)
    return w, magnitude, phase

# FIR Filter Design
def design_fir_filter(num_taps, cutoff, fs, filter_type="lowpass"):
    if num_taps <= 0:
        raise ValueError("num_taps must be greater than 0")
    if filter_type == "lowpass":
        b = firwin(
            num_taps,
            cutoff,
            fs=fs,
            pass_zero=True
        )
    elif filter_type == "highpass":
        b = firwin(
            num_taps,
            cutoff,
            fs=fs,
            pass_zero=False
        )
    elif filter_type == "bandpass":
        b = firwin(
            num_taps,
            cutoff,
            fs=fs,
            pass_zero=False
        )
    elif filter_type == "bandstop":
        b = firwin(
            num_taps,
            cutoff,
            fs=fs,
            pass_zero=True
        )
    else:
        raise ValueError(
            "filter_type must be "
            "'lowpass', 'highpass', 'bandpass' or 'bandstop'"
        )
    return b


# Apply FIR Filter
def apply_fir_filter(x, b):
    y = np.convolve(x, b, mode="same")
    return y

# IIR Design - Impulse Invariance
def design_iir_impulse(order, cutoff, fs, filter_type="lowpass"):
    if filter_type == "lowpass":
        wc = 2 * np.pi * cutoff
        b_a, a_a = butter(
            order,
            wc,
            btype="lowpass",
            analog=True
        )
    elif filter_type == "bandpass":
        wc = [
            2 * np.pi * cutoff[0],
            2 * np.pi * cutoff[1]
        ]
        b_a, a_a = butter(
            order,
            wc,
            btype="bandpass",
            analog=True
        )
    else:
        raise ValueError(
            "Impulse invariance supports "
            "'lowpass' and 'bandpass'"
        )
    b, a, dt = cont2discrete(
        (b_a, a_a),
        dt=1 / fs,
        method="impulse"
    )
    return b.flatten(), a


# IIR Design - Bilinear Transformation
def design_iir_bilinear(order, cutoff, fs, filter_type="highpass"):
    if filter_type == "highpass":
        wc = 2 * np.pi * cutoff
        b_a, a_a = butter(
            order,
            wc,
            btype="highpass",
            analog=True
        )

    elif filter_type == "bandstop":
        wc = [
            2 * np.pi * cutoff[0],
            2 * np.pi * cutoff[1]
        ]
        b_a, a_a = butter(
            order,
            wc,
            btype="bandstop",
            analog=True
        )
    else:
        raise ValueError(
            "Bilinear transformation supports "
            "'highpass' and 'bandstop'"
        )
    b, a = bilinear(
        b_a,
        a_a,
        fs=fs
    )
    return b, a


# Apply IIR Filter
def apply_iir_filter(x, b, a):
    y = np.zeros(len(x))
    for n in range(len(x)):
        for k in range(len(b)):
            if n - k >= 0:
                y[n] += b[k] * x[n - k]
        for k in range(1, len(a)):
            if n - k >= 0:
                y[n] -= a[k] * y[n - k]
        y[n] /= a[0]
    return y


# IIR Frequency Response
def iir_frequency_response(b, a, fs):
    w, h = freqz(
        b,
        a,
        fs=fs
    )
    magnitude = np.abs(h)
    phase = np.angle(h)
    return w, magnitude, phase

def plot_signal(t, x, title="Signal"):
    plt.figure(figsize=(10, 4))
    plt.plot(t, x)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_fft(x, fs, title="Frequency Spectrum"):
    magnitude, frequency = compute_fft(x, fs)

    plt.figure(figsize=(10, 4))
    plt.plot(frequency, magnitude)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_sampling(t_org, x_org, ts, x_samp):
    plt.figure(figsize=(10, 5))

    plt.plot(t_org, x_org, label="Original Signal")
    plt.stem(ts, x_samp, linefmt="C1-", markerfmt="C1o",
             basefmt=" ", label="Samples")

    plt.title("Sampling")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_filter_response(w, magnitude, phase, title="Filter Response"):

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.plot(w, magnitude)
    plt.title(title + " - Magnitude")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(w, phase)
    plt.title(title + " - Phase")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (rad)")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def plot_filter_comparison(t, x, y, title="Filter Comparison"):

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.plot(t, x)
    plt.title("Original Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(t, y)
    plt.title("Filtered Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    