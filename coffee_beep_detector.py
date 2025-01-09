import sounddevice as sd
import numpy as np
from scipy.signal import find_peaks

def detect_beep(indata, frames, time, status):
    # Convert audio data to mono if stereo
    if len(indata.shape) == 2:
        audio_data = indata[:, 0]
    else:
        audio_data = indata
    
    # Calculate frequency spectrum
    spectrum = np.abs(np.fft.rfft(audio_data))
    frequencies = np.fft.rfftfreq(len(audio_data), 1 / SAMPLE_RATE)
    
    # Look for peaks in typical beep frequency range (1000-4000 Hz)
    beep_range = (frequencies >= 1000) & (frequencies <= 4000)
    peaks, _ = find_peaks(spectrum[beep_range], height=0.1)
    
    if len(peaks) > 0:
        print("BEEP DETECTED")

# Audio stream parameters
SAMPLE_RATE = 44100
BLOCK_SIZE = 2048

try:
    # Start continuous audio stream
    with sd.InputStream(callback=detect_beep,
                       channels=1,
                       samplerate=SAMPLE_RATE,
                       blocksize=BLOCK_SIZE):
        print("Listening for beeps... Press Ctrl+C to stop")
        while True:
            sd.sleep(100)  # Keep the stream running

except KeyboardInterrupt:
    print("\nStopping beep detection")
except Exception as e:
    print(f"Error: {str(e)}") 
