import numpy as np
from main import (
    generate_sine,
    composite_signal,
    compute_fft,
    sample_signal,
    check_aliasing,
    aliased_frequency,
    reconstruct_signal,
    linear_convolution,
    moving_average_filter,
    add_noise,
    filter_frequency_response,
    design_fir_filter,
    apply_fir_filter,
    design_iir_impulse,
    design_iir_bilinear,
    apply_iir_filter,
    iir_frequency_response
)


# Test 1: Sine Wave Generation
def test_generate_sine():
    t, x = generate_sine(1, 10, 1000, 1)

    assert len(t) == len(x)
    assert np.max(x) <= 1
    assert np.min(x) >= -1

    print("generate_sine() : PASS")


# Test 2: Composite Signal
def test_composite_signal():
    t1, x1 = generate_sine(1, 10, 100, 1)
    t2, x2 = generate_sine(1, 20, 100, 1)

    t, x = composite_signal(x1, t1, x2, t2)

    assert len(t) == len(x)
    assert np.allclose(x, x1 + x2)

    print("composite_signal() : PASS")


# Test 3: FFT
def test_fft():
    fs = 1000
    t, x = generate_sine(1, 50, fs, 1)

    magnitude, frequency = compute_fft(x, fs)

    peak_frequency = abs(frequency[np.argmax(magnitude)])

    assert np.isclose(peak_frequency, 50)

    print("compute_fft() : PASS")


# Test 4: Sampling
def test_sampling():
    t_org, x_org, ts, x_samp = sample_signal(
        1, 10, 100, 1
    )

    assert len(t_org) > len(ts)
    assert len(ts) == len(x_samp)

    print("sample_signal() : PASS")


# Test 5: Nyquist Check
def test_aliasing_check():

    assert check_aliasing(60, 100) == True
    assert check_aliasing(40, 100) == False

    print("check_aliasing() : PASS")


# Test 6: Aliased Frequency
def test_aliased_frequency():

    assert aliased_frequency(80, 100) == 20
    assert aliased_frequency(120, 100) == 20

    print("aliased_frequency() : PASS")


# Test 7: Reconstruction
def test_reconstruction():

    t_old = np.array([0, 1, 2])
    x_old = np.array([0, 1, 0])

    t_new = np.array([0, 0.5, 1, 1.5, 2])

    x_new = reconstruct_signal(
        t_old,
        x_old,
        t_new
    )

    assert len(x_new) == len(t_new)

    print("reconstruct_signal() : PASS")


# Test 8: Linear Convolution
def test_linear_convolution():

    x = np.array([1, 2, 3])
    h = np.array([1, 1])

    y = linear_convolution(x, h)

    expected = np.array([1, 3, 5, 3])

    assert np.array_equal(y, expected)

    print("linear_convolution() : PASS")


# Test 9: Moving Average
def test_moving_average():

    x = np.array([1, 2, 3, 4, 5])

    y = moving_average_filter(x, 3)

    expected = np.array([2, 3, 4])

    assert np.allclose(y, expected)

    print("moving_average_filter() : PASS")


# Test 10: Noise
def test_noise():

    x = np.zeros(1000)

    noisy = add_noise(x, 1)

    assert len(noisy) == len(x)
    assert not np.array_equal(noisy, x)

    print("add_noise() : PASS")


# Test 11: FIR Filter Design
def test_fir_design():

    fs = 1000

    b = design_fir_filter(
        51,
        100,
        fs,
        "lowpass"
    )

    assert len(b) == 51

    print("design_fir_filter() : PASS")


# Test 12: FIR Filter Application
def test_fir_filter():

    x = np.ones(100)
    b = design_fir_filter(
        21,
        100,
        1000,
        "lowpass"
    )

    y = apply_fir_filter(x, b)

    assert len(y) == len(x)

    print("apply_fir_filter() : PASS")


# Test 13: FIR Frequency Response
def test_fir_frequency_response():

    b = design_fir_filter(
        51,
        100,
        1000,
        "lowpass"
    )

    w, magnitude, phase = filter_frequency_response(
        b,
        1000
    )

    assert len(w) == len(magnitude)
    assert len(w) == len(phase)

    print("filter_frequency_response() : PASS")


# Test 14: IIR Impulse Invariance
def test_iir_impulse():

    b, a = design_iir_impulse(
        4,
        100,
        1000,
        "lowpass"
    )

    assert len(b) > 0
    assert len(a) > 0

    print("design_iir_impulse() : PASS")


# Test 15: IIR Bilinear Transformation
def test_iir_bilinear():

    b, a = design_iir_bilinear(
        4,
        100,
        1000,
        "highpass"
    )

    assert len(b) > 0
    assert len(a) > 0

    print("design_iir_bilinear() : PASS")


# Test 16: IIR Filter Application
def test_iir_filter():

    x = np.ones(100)

    b, a = design_iir_bilinear(
        4,
        100,
        1000,
        "highpass"
    )

    y = apply_iir_filter(x, b, a)

    assert len(y) == len(x)
    assert np.all(np.isfinite(y))

    print("apply_iir_filter() : PASS")


# Test 17: IIR Frequency Response
def test_iir_frequency_response():

    b, a = design_iir_bilinear(
        4,
        100,
        1000,
        "highpass"
    )

    w, magnitude, phase = iir_frequency_response(
        b,
        a,
        1000
    )

    assert len(w) == len(magnitude)
    assert len(w) == len(phase)

    print("iir_frequency_response() : PASS")


# Run all tests
if __name__ == "__main__":

    print("\nRunning SignalLab Phase 2 Tests...\n")

    test_generate_sine()
    test_composite_signal()
    test_fft()
    test_sampling()
    test_aliasing_check()
    test_aliased_frequency()
    test_reconstruction()
    test_linear_convolution()
    test_moving_average()
    test_noise()
    test_fir_design()
    test_fir_filter()
    test_fir_frequency_response()
    test_iir_impulse()
    test_iir_bilinear()
    test_iir_filter()
    test_iir_frequency_response()

    print("\nAll tests completed!")