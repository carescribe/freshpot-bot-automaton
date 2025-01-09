import sounddevice as sd
import numpy as np
from scipy.signal import find_peaks
import soundfile as sf

LOWER_FREQ=3500
UPPER_FREQ=4200
np.set_printoptions(threshold=np.inf)

# Add these global variables
all_audio_data = []
CHANNELS = 1

def detect_beep(indata, frames, time, status):
    global all_audio_data
    
    # Store the audio data
    # all_audio_data.append(indata.copy())
    
    # Convert audio data to mono if stereo
    if len(indata.shape) == 2:
        audio_data = indata[:, 0]
    else:
        audio_data = indata
    
    # Calculate frequency spectrum
    spectrum = np.abs(np.fft.rfft(audio_data))
    frequencies = np.fft.rfftfreq(len(audio_data), 1 / SAMPLE_RATE)
    print("frequencies: ", frequencies[0])
    
    # Look for peaks in typical beep frequency range (1000-4000 Hz)
    beep_range = (frequencies >= LOWER_FREQ) & (frequencies <= UPPER_FREQ)
#    print(f"{beep_range}")
    peaks, _ = find_peaks(spectrum[beep_range], height=0.1)
#    print(peaks)
    
    if len(peaks) > 0:
        print("BEEP DETECTED")

# Audio stream parameters
SAMPLE_RATE = 44100
BLOCK_SIZE = 10000

try:
    # Start continuous audio stream
    with sd.InputStream(callback=detect_beep,
                       channels=CHANNELS,
                       samplerate=SAMPLE_RATE,
                       blocksize=BLOCK_SIZE):
        print("Listening for beeps... Press Ctrl+C to stop")
        while True:
            sd.sleep(100)

except KeyboardInterrupt:
    print("\nStopping beep detection")
    # # Save the recorded audio to file
    # if all_audio_data:
    #     audio_data = np.concatenate(all_audio_data, axis=0)
    #     sf.write('coffee.wav', audio_data, SAMPLE_RATE)
    #     print("Audio saved to coffee.wav")
except Exception as e:
    print(f"Error: {str(e)}") 
