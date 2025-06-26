"""
Moving Average Filter - DSP Implementation
==========================================

This module demonstrates the implementation of a moving average filter,
which is a simple Linear-Time-Invariant (LTI) system commonly used in
Digital Signal Processing for noise reduction and signal smoothing.

The moving average filter computes the average of a fixed number of
input samples to produce each output sample.

Author: DSP Student
Date: June 26, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import math

class MovingAverageFilter:
    """
    A class to implement and demonstrate moving average filters
    """
    
    def __init__(self, window_size):
        """
        Initialize the moving average filter
        
        Parameters:
        window_size (int): Number of samples to average (filter length)
        """
        self.window_size = window_size
        self.buffer = np.zeros(window_size)
        self.index = 0
        self.sum = 0.0
        
    def filter_sample(self, input_sample):
        """
        Process a single input sample through the moving average filter
        
        Parameters:
        input_sample (float): Input sample value
        
        Returns:
        float: Filtered output sample
        """
        # Remove the oldest sample from the sum
        self.sum -= self.buffer[self.index]
        
        # Add the new sample
        self.buffer[self.index] = input_sample
        self.sum += input_sample
        
        # Update circular buffer index
        self.index = (self.index + 1) % self.window_size
        
        # Return the average
        return self.sum / self.window_size
    
    def filter_signal(self, input_signal):
        """
        Process an entire signal through the moving average filter
        
        Parameters:
        input_signal (array): Input signal array
        
        Returns:
        array: Filtered output signal
        """
        output_signal = np.zeros_like(input_signal)
        
        for i, sample in enumerate(input_signal):
            output_signal[i] = self.filter_sample(sample)
            
        return output_signal
    
    def get_impulse_response(self):
        """
        Get the impulse response of the moving average filter
        
        Returns:
        array: Impulse response
        """
        return np.ones(self.window_size) / self.window_size
    
    def get_frequency_response(self, num_points=1024):
        """
        Calculate the frequency response of the moving average filter
        
        Parameters:
        num_points (int): Number of frequency points to calculate
        
        Returns:
        tuple: (frequencies, magnitude response, phase response)
        """
        h = self.get_impulse_response()
        w, H = signal.freqz(h, worN=num_points)
        
        # Convert to Hz (assuming normalized frequency)
        frequencies = w / (2 * np.pi)
        magnitude = np.abs(H)
        phase = np.angle(H)
        
        return frequencies, magnitude, phase

def create_test_signal(duration=2.0, fs=1000):
    """
    Create a test signal with noise for demonstration
    
    Parameters:
    duration (float): Signal duration in seconds
    fs (int): Sampling frequency in Hz
    
    Returns:
    tuple: (time array, clean signal, noisy signal)
    """
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    # Create a composite signal with multiple frequency components
    clean_signal = (2 * np.sin(2 * np.pi * 10 * t) +        # 10 Hz sine wave
                   1.5 * np.sin(2 * np.pi * 25 * t) +       # 25 Hz sine wave
                   0.8 * np.sin(2 * np.pi * 50 * t))        # 50 Hz sine wave
    
    # Add noise
    noise = 1.5 * np.random.randn(len(t))
    noisy_signal = clean_signal + noise
    
    return t, clean_signal, noisy_signal

def demonstrate_moving_average():
    """
    Demonstrate the moving average filter with various window sizes
    """
    print("Moving Average Filter Demonstration")
    print("=" * 40)
    
    # Create test signals
    t, clean_signal, noisy_signal = create_test_signal()
    
    # Test different window sizes
    window_sizes = [5, 15, 30, 60]
    
    # Create subplots
    fig, axes = plt.subplots(3, 2, figsize=(15, 12))
    fig.suptitle('Moving Average Filter Analysis', fontsize=16)
    
    # Plot original signals
    axes[0, 0].plot(t[:500], clean_signal[:500], 'b-', label='Clean Signal', linewidth=2)
    axes[0, 0].plot(t[:500], noisy_signal[:500], 'r-', alpha=0.7, label='Noisy Signal')
    axes[0, 0].set_title('Original Signals (First 0.5s)')
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Amplitude')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot filtered signals with different window sizes
    colors = ['green', 'orange', 'purple', 'brown']
    axes[0, 1].plot(t[:500], clean_signal[:500], 'b-', label='Clean Signal', linewidth=2)
    
    for i, window_size in enumerate(window_sizes):
        # Create and apply filter
        ma_filter = MovingAverageFilter(window_size)
        filtered_signal = ma_filter.filter_signal(noisy_signal)
        
        axes[0, 1].plot(t[:500], filtered_signal[:500], color=colors[i], 
                       label=f'MA Filter (N={window_size})', alpha=0.8)
        
        print(f"Window Size: {window_size}")
        mse = np.mean((clean_signal - filtered_signal)**2)
        print(f"  Mean Squared Error: {mse:.4f}")
    
    axes[0, 1].set_title('Filtered Signals Comparison (First 0.5s)')
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Amplitude')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot impulse responses
    for i, window_size in enumerate(window_sizes):
        ma_filter = MovingAverageFilter(window_size)
        impulse_response = ma_filter.get_impulse_response()
        axes[1, 0].stem(range(len(impulse_response)), impulse_response, 
                       linefmt=colors[i], markerfmt='o', basefmt=' ',
                       label=f'N={window_size}')
    
    axes[1, 0].set_title('Impulse Responses')
    axes[1, 0].set_xlabel('Sample Index (n)')
    axes[1, 0].set_ylabel('Amplitude')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot frequency responses (magnitude)
    for i, window_size in enumerate(window_sizes):
        ma_filter = MovingAverageFilter(window_size)
        frequencies, magnitude, phase = ma_filter.get_frequency_response()
        axes[1, 1].plot(frequencies, 20 * np.log10(magnitude + 1e-10), 
                       color=colors[i], label=f'N={window_size}')
    
    axes[1, 1].set_title('Frequency Response (Magnitude)')
    axes[1, 1].set_xlabel('Normalized Frequency')
    axes[1, 1].set_ylabel('Magnitude (dB)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_ylim([-60, 5])
    
    # Plot frequency responses (phase)
    for i, window_size in enumerate(window_sizes):
        ma_filter = MovingAverageFilter(window_size)
        frequencies, magnitude, phase = ma_filter.get_frequency_response()
        axes[2, 0].plot(frequencies, np.degrees(phase), 
                       color=colors[i], label=f'N={window_size}')
    
    axes[2, 0].set_title('Frequency Response (Phase)')
    axes[2, 0].set_xlabel('Normalized Frequency')
    axes[2, 0].set_ylabel('Phase (degrees)')
    axes[2, 0].legend()
    axes[2, 0].grid(True, alpha=0.3)
    
    # Plot pole-zero diagram for N=15
    ma_filter = MovingAverageFilter(15)
    h = ma_filter.get_impulse_response()
    
    # For moving average filter: H(z) = (1/N) * (1 - z^(-N)) / (1 - z^(-1))
    # Zeros at z = exp(j*2*pi*k/N) for k = 1, 2, ..., N-1
    # Poles at z = 0 (N-1 poles at origin)
    
    N = 15
    zeros = []
    for k in range(1, N):
        zeros.append(np.exp(1j * 2 * np.pi * k / N))
    
    # Plot unit circle
    theta = np.linspace(0, 2*np.pi, 1000)
    unit_circle_x = np.cos(theta)
    unit_circle_y = np.sin(theta)
    
    axes[2, 1].plot(unit_circle_x, unit_circle_y, 'k--', alpha=0.5, label='Unit Circle')
    
    # Plot zeros
    zeros_real = [z.real for z in zeros]
    zeros_imag = [z.imag for z in zeros]
    axes[2, 1].scatter(zeros_real, zeros_imag, marker='o', s=50, c='red', label='Zeros')
    
    # Plot poles at origin
    axes[2, 1].scatter([0], [0], marker='x', s=100, c='blue', label=f'Poles (N-1={N-1})')
    
    axes[2, 1].set_title(f'Pole-Zero Plot (N={N})')
    axes[2, 1].set_xlabel('Real Part')
    axes[2, 1].set_ylabel('Imaginary Part')
    axes[2, 1].legend()
    axes[2, 1].grid(True, alpha=0.3)
    axes[2, 1].set_xlim([-1.5, 1.5])
    axes[2, 1].set_ylim([-1.5, 1.5])
    axes[2, 1].set_aspect('equal')
    
    plt.tight_layout()
    plt.show()

def demonstrate_real_time_filtering():
    """
    Demonstrate real-time sample-by-sample filtering
    """
    print("\nReal-time Filtering Demonstration")
    print("=" * 40)
    
    # Create a simple test signal
    fs = 100  # Sampling frequency
    duration = 1.0  # Duration in seconds
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    # Create signal: sine wave + noise
    clean_signal = np.sin(2 * np.pi * 5 * t)  # 5 Hz sine wave
    noise = 0.5 * np.random.randn(len(t))
    noisy_signal = clean_signal + noise
    
    # Initialize filter
    ma_filter = MovingAverageFilter(window_size=10)
    
    # Process samples one by one (simulating real-time)
    filtered_samples = []
    
    print("Processing samples in real-time...")
    for i, sample in enumerate(noisy_signal):
        filtered_sample = ma_filter.filter_sample(sample)
        filtered_samples.append(filtered_sample)
        
        if i % 20 == 0:  # Print every 20th sample
            print(f"Sample {i:3d}: Input = {sample:6.3f}, Output = {filtered_sample:6.3f}")
    
    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(t, clean_signal, 'b-', label='Clean Signal', linewidth=2)
    plt.plot(t, noisy_signal, 'r-', alpha=0.7, label='Noisy Signal')
    plt.plot(t, filtered_samples, 'g-', label='Filtered Signal', linewidth=2)
    plt.title('Real-time Moving Average Filtering')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    # Run the demonstrations
    demonstrate_moving_average()
    demonstrate_real_time_filtering()
    
    print("\nMoving Average Filter Properties:")
    print("=" * 40)
    print("• Low-pass filter characteristics")
    print("• Linear phase response (constant group delay)")
    print("• Simple implementation (only addition and division)")
    print("• Larger window size → better noise reduction but more delay")
    print("• Smaller window size → less smoothing but faster response")
    print("• Transfer function: H(z) = (1/N) * (1 - z^(-N)) / (1 - z^(-1))")
    print("• Impulse response: h[n] = 1/N for 0 ≤ n ≤ N-1, 0 otherwise")
