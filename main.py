import matplotlib.pyplot as plt
import numpy as np


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
    np.convolve(x,h)