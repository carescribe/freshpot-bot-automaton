import pyaudio
import wave

def record_audio(filename, duration=5, sample_rate=44100, channels=1, chunk=1024):
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    
    # Open stream
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk
    )
    
    print("Recording...")
    frames = []
    
    # Record for the specified duration
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("Finished recording!")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Save the recorded data as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

if __name__ == "__main__":
    # Record 5 seconds of audio and save it to 'output.wav'
    record_audio("output.wav", duration=5)
