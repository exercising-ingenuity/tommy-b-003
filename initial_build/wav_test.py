import wave
import sys
import pyaudio

def play_audio(file_path):
    # Open the audio file
    wf = wave.open(file_path, 'rb')
    
    # Create PyAudio instance
    p = pyaudio.PyAudio()
    
    # Open a stream to play audio
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    # Read and play audio data
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
        
    # Stop and close the stream and PyAudio instance
    stream.stop_stream()
    stream.close()
    p.terminate()
    
wav_filepath = '/home/tommy_b/openai/testing/i_see_you.wav'

play_audio(wav_filepath)
	
