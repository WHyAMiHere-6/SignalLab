from main import *

# Generate a composite signal
t1, x1 = generate_sine(1, 10, 1000, 1)
t2, x2 = generate_sine(0.5, 100, 1000, 1)

t, x = composite_signal(x1, t1, x2, t2)

# Plot original signal
plot_signal(t, x, "Composite Signal")

# Plot FFT
plot_fft(x, 1000, "Composite Signal Spectrum")

# Design FIR low-pass filter
b = design_fir_filter(
    num_taps=51,
    cutoff=50,
    fs=1000,
    filter_type="lowpass"
)

# Apply filter
y = apply_fir_filter(x, b)

# Filter frequency response
w, magnitude, phase = filter_frequency_response(b, 1000)

# Plot filter response
plot_filter_response(
    w,
    magnitude,
    phase,
    "FIR Low-Pass Filter"
)

# Compare original and filtered
plot_filter_comparison(
    t,
    x,
    y,
    "Low-Pass Filtering"
)