#======================================================
#Audio Recognition Rough Code
#Calculate Speech Rate
#======================================================

#------------------------------------------------------
#INSTALLS
#------------------------------------------------------
#pip install pyaudio speechrecognition

#------------------------------------------------------
#LIBRARIES
#------------------------------------------------------
#-audio processing
import pyaudio
import wave
import speech_recognition as sr
#-interface
import tkinter as tk
from tkinter import ttk
#-threading & other
import threading
import time
import queue
import os
import tempfile

#------------------------------------------------------
#CONST DATA, PATHS, & INITIALIZATIONS
#------------------------------------------------------
r = sr.Recognizer() #initialize recognizer

#------------------------------------------------------
#FUNCTIONS
#------------------------------------------------------
#calculate_speech_rate(): 
def calculate_speech_rate(text, duration):
    words = text.split()
    num_words = len(words)
    speech_rate = num_words / duration
    return speech_rate

#------------------------------------------------------
#STATIC NO INTERFACE
#------------------------------------------------------
#audio source = default microphone
#with sr.Microphone() as source:
#    print("Please speak into the microphone.")
    
#    #adjust the recognizer sensitivity to ambient noise
#    r.adjust_for_ambient_noise(source)
    
#    #record audio for a fixed duration (e.g., 5 seconds)
#    start_time = time.time()
#    audio = r.listen(source, phrase_time_limit=5)
#    end_time = time.time()

#    #duration of speech
#    duration = end_time - start_time

#try:
#    #uses Google Web Speech API to recognize audio
#    text = r.recognize_google(audio)
#    print("You said: " + text)
    
#    #Calculates and prints speech rate
#    speech_rate = calculate_speech_rate(text, duration)
#    print(f"Your speech rate is: {speech_rate:.2f} words per second")
#except sr.UnknownValueError:
#    print("Google Speech Recognition could not understand audio")
#except sr.RequestError as e:
#    print(f"Could not request results from Google Speech Recognition service; {e}")


#------------------------------------------------------
##STATIC WITH INTERFACE
#------------------------------------------------------
#class SpeechRateApp:
#    def __init__(self, master):
#        self.master = master
#        master.title("Speech Rate Detector")

#        self.state = "stopped"
#        self.recognizer = sr.Recognizer()
#        self.microphone = sr.Microphone()
#        self.speech_duration = 0
#        self.start_time = 0

#        # Initialize GUI elements
#        self.start_button = tk.Button(master, text="Start Recording", command=self.start_recording)
#        self.start_button.pack()

#        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
#        self.stop_button.pack()

#        self.status_label = tk.Label(master, text="Press 'Start Recording' to begin.", wraplength=400)
#        self.status_label.pack()

#    def start_recording(self):
#        self.state = "recording"
#        self.start_button.config(state=tk.DISABLED)
#        self.stop_button.config(state=tk.NORMAL)
#        self.status_label.config(text="Recording... Speak now.")
#        self.start_time = time.time()
#        Thread(target=self.record).start()

#    def stop_recording(self):
#        self.state = "stopped"
#        self.stop_button.config(state=tk.DISABLED)
#        self.start_button.config(state=tk.NORMAL)
#        self.status_label.config(text="Processing... Please wait.")

#    def record(self):
#        with self.microphone as source:
#            self.recognizer.adjust_for_ambient_noise(source)
#            audio = self.recognizer.listen(source)
#        self.process_audio(audio)

#    def process_audio(self, audio):
#        #stop recording and process the audio
#        try:
#            self.speech_duration = time.time() - self.start_time
#            text = self.recognizer.recognize_google(audio)
#            speech_rate = len(text.split()) / self.speech_duration
#            self.status_label.config(text=f"You said: {text}\nSpeech rate: {speech_rate:.2f} words per second.")
#        except sr.UnknownValueError:
#            self.status_label.config(text="Could not understand audio.")
#        except sr.RequestError as e:
#            self.status_label.config(text=f"Could not request results; {e}")

#if __name__ == "__main__":
#    root = tk.Tk()
#    app = SpeechRateApp(root)
#    root.mainloop()

#------------------------------------------------------
#LIVE WITH INTERFACE
#------------------------------------------------------
class SpeechRateApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Real-Time Speech Rate Detector")
        self.geometry("800x400")

        self.start_button = ttk.Button(self, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=20)

        self.stop_button = ttk.Button(self, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=20)
        self.stop_button["state"] = "disabled"

        self.status_label = ttk.Label(self, text="Press 'Start Recording' to begin.", wraplength=760)
        self.status_label.pack(pady=20)

        self.recording = False
        self.queue = queue.Queue()

    def start_recording(self):
        self.recording = True
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "normal"
        self.status_label["text"] = "Recording... Speak into the microphone."
        threading.Thread(target=self.record_audio, daemon=True).start()
        threading.Thread(target=self.process_audio, daemon=True).start()

    def stop_recording(self):
        self.recording = False
        self.start_button["state"] = "normal"
        self.stop_button["state"] = "disabled"
        self.status_label["text"] = "Processing last chunk..."

    def record_audio(self):
        chunk_size = 1024  #frames per buffer
        sample_format = pyaudio.paInt16  #16 bits per sample
        channels = 1
        
        rate = 44100  #sample rate
        record_seconds = 5  #ideal audio chunk duration (in seconds)
        frames_per_5_seconds = int(rate * record_seconds)  #frames for a 5-second chunk
        
        p = pyaudio.PyAudio()
        stream = p.open(format=sample_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)  
    
        while self.recording:
            frames = []
            for _ in range(0, int(rate / chunk_size * record_seconds)):
                data = stream.read(chunk_size)
                frames.append(data)
            self.queue.put(b''.join(frames))  #place 5-second chunk into queue
    
        stream.stop_stream()
        stream.close()
        p.terminate()
    
        #signal: recording is complete
        self.queue.put(None)

    def update_status_label(self, text):
        self.status_label["text"] = text #executed by main thread
    
    def process_audio(self):
        r = sr.Recognizer()
        while self.recording or not self.queue.empty():
            audio_data_chunk = self.queue.get()
            if audio_data_chunk is None:
                break
            try:
                #create temp file to store audio chunk
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
                    wf = wave.open(tmpfile.name, 'wb')
                    wf.setnchannels(1)
                    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
                    wf.setframerate(44100)
                    wf.writeframes(audio_data_chunk)
                    wf.close()
                    #use temp file with speech_recognition
                    with sr.AudioFile(tmpfile.name) as source:
                        audio_data = r.record(source)
                        text = r.recognize_google(audio_data)
                        words = text.split()
                        num_words = len(words)
                        #calculate duration using fixed chunk size & rate
                        duration = len(audio_data_chunk) / (44100 * 2)  #2 bytes per sample (16-bit)
                        speech_rate = num_words / duration
                        message = f"RECOGNIZED TEXT: {text}\n\n Processed chunk: {num_words} words in {duration:.2f} seconds, speech rate: {speech_rate:.2f} words/second"
                        print(message)
                        self.after(0, self.update_status_label, message)
            except sr.UnknownValueError:
                self.after(0, self.update_status_label, "Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                self.after(0, self.update_status_label, f"Could not request results from Speech Recognition service; {e}")
            finally:
                os.remove(tmpfile.name) #ensure temp file is deleted
    
        self.after(0, self.update_status_label, "Finished processing audio. Recording stopped.")

if __name__ == "__main__":
    app = SpeechRateApp()
    app.mainloop()

#------------------------------------------------------
# #alternative time calculation for audio buffering
#------------------------------------------------------
#    def record_audio(self):
#         chunk_size = 1024  # Frames per buffer
#         sample_format = pyaudio.paInt16  # 16 bits per sample
#         channels = 1
#         rate = 44100  # Sample rate
#         record_seconds = 5  # Target duration for audio chunks
    
#         p = pyaudio.PyAudio()
#         stream = p.open(format=sample_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
    
#         while self.recording:
#             frames = []
#             start_time = time.time()
#             while time.time() - start_time < record_seconds:
#                 data = stream.read(chunk_size)
#                 frames.append(data)
#             self.queue.put(b''.join(frames))  # Place the 5-second chunk into the queue
    
#         stream.stop_stream()
#         stream.close()
#         p.terminate()
    
#         # Signal that recording is complete
#         self.queue.put(None)


