import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import freqz,firwin,butter,cont2discrete,bilinear

# Generation of Sine Wave
def generate_sine(A, f, fs, duration, phase):
    t = np.arange(0, duration, 1/fs)
    x = A * np.sin(2*np.pi*f*t + phase)
    return t, x


# Composite Signal
def composite_signal(x1, t1, x2, t2):



    # If both time axes are identical, directly add the signals
    if np.array_equal(t1, t2):
        x_comp = x1 + x2
        return t1, x_comp

    # Interpolate the signal with fewer samples
    if len(t1) > len(t2):
        int_x2 = np.interp(t1, t2, x2)
        x_comp = x1 + int_x2
        return t1, x_comp

    else:
        int_x1 = np.interp(t2, t1, x1)
        x_comp = int_x1 + x2
        return t2, x_comp

def compute_fft(x, fs):
    X=np.fft.fft(x)
    f=np.fft.fftfreq(len(x),1/fs)
    magnitude=np.abs(X)
    return magnitude,f

def sample_signal(A, f, fs, duration):
    t_org=np.arange(0,duration,1/(100*f))
    ts=np.arange(0,duration,1/fs)
    x_samp=A*np.sin(2*np.pi*f*ts)
    x_org=A*np.sin(2*np.pi*f*t_org)
    if check_aliasing(f,fs):
        print("Nyquist Theorem Not Satisfied")
        
    else:
        print("Nyquist Theorem Satisfied")
    return t_org,x_org,ts,x_samp
        
def check_aliasing(f,fs):
    if 2*f>fs:
        return True
    else:
        return False

def aliased_frequency(f, fs):
    f_alias = f % fs
    if f_alias > fs/2:
        f_alias=fs-f_alias
    return f_alias

def reconstruct_signal(t_old,x_old,t_new):
    x_new=np.interp(t_new,t_old,x_old)
    return x_new

def linear_convolution(x, h):
    y=np.convolve(x,h)
    return y

def moving_average_filter(x, N):
    y = np.convolve(x, np.ones(N) / N, mode='valid')
    return y

def add_noise(x, noise_level):
    noise = np.random.normal(0, noise_level, len(x))
    return x + noise

def filter_frequency_response(b):
    w, h = freqz(b)
    magnitude = np.abs(h)
    phase = np.angle(h)

    return w, magnitude, phase
def design_fir_filter(num_taps, cutoff, fs, filter_type="lowpass"):
    if filter_type == "lowpass":
        b = firwin(num_taps, cutoff, fs=fs, pass_zero=True)

    elif filter_type == "highpass":
        b = firwin(num_taps, cutoff, fs=fs, pass_zero=False)

    elif filter_type == "bandpass":
        b = firwin(num_taps, cutoff, fs=fs, pass_zero=False)

    elif filter_type == "bandstop":
        b = firwin(num_taps, cutoff, fs=fs, pass_zero=True)

    else:
        raise ValueError("Invalid filter type")

    return b

def apply_fir_filter(x, b):
    y = np.convolve(x, b, mode="same")
    return y

def design_iir_impulse(order, cutoff, fs, filter_type="lowpass"):
    if filter_type == "lowpass":
        wc = 2 * np.pi * cutoff
        b_a, a_a = butter(order, wc, btype="lowpass", analog=True)

    elif filter_type == "bandpass":
        wc = [2 * np.pi * cutoff[0], 2 * np.pi * cutoff[1]]
        b_a, a_a = butter(order, wc, btype="bandpass", analog=True)

    else:
        raise ValueError("Use lowpass or bandpass")

    bz, az, dt = cont2discrete(
        (b_a, a_a),
        dt=1/fs,
        method="impulse"
    )

    return bz.flatten(), az

def design_iir_bilinear(order, cutoff, fs, filter_type="highpass"):
    if filter_type == "highpass":
        wc = 2 * np.pi * cutoff
        b_a, a_a = butter(order, wc, btype="highpass", analog=True)

    elif filter_type == "bandstop":
        wc = [2 * np.pi * cutoff[0],
              2 * np.pi * cutoff[1]]
        b_a, a_a = butter(order, wc, btype="bandstop", analog=True)

    else:
        raise ValueError("Use highpass or bandstop")

    b, a = bilinear(b_a, a_a, fs=fs)

    return b, a 

def apply_iir_filter(x, b, a):
    y = np.zeros(len(x))

    for n in range(len(x)):
        for k in range(len(b)):
            if n - k >= 0:
                y[n] += b[k] * x[n-k]

        for k in range(1, len(a)):
            if n - k >= 0:
                y[n] -= a[k] * y[n-k]

        y[n] /= a[0]

    return y

def iir_frequency_response(b, a, fs):
    w, h = freqz(b, a, fs=fs)

    magnitude = np.abs(h)
    phase = np.angle(h)

    return w, magnitude, phase
