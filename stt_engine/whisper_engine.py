### translingo/stt_engine/whisper_engine.py
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import whisper
import os
# import tempfile
import queue
import threading
import time

class WhisperRecognizer:
    def __init__(self, isPipeline=False, default_model_size="base"):
        self.SAMPLE_RATE = 16000
        self.CHUNK_DURATION = 3
        self.CHUNK_SIZE = int(self.SAMPLE_RATE * self.CHUNK_DURATION)
        self.OVERLAP = 0#.5
        self.audio_q = queue.Queue(maxsize=5)
        if isPipeline:
            self.model = whisper.load_model(default_model_size)
        else:
            self.model = self.load_selected_model() # whisper.load_model(model_size)
        self.transcripts = []
        self.last_text = ""
        self.display_mic_info()


    def test_input_devices(self):
        for i, dev in enumerate(sd.query_devices()):
            if dev['max_input_channels'] > 0:
                print(f"Testing input device {i}: {dev['name']}")
                try:
                    duration = 1  # seconds
                    fs = 16000
                    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16', device=i)
                    sd.wait()
                    if np.any(audio):
                        print(f"✅ Device {i} picked up sound.")
                    else:
                        print(f"⚠️ Device {i} recorded silence.")
                except Exception as e:
                    print(f"❌ Device {i} error: {e}")

    def display_mic_info(self):
        print("Default input device:", sd.default.device)
        print(sd.query_devices())
        return

    def run_pipeline_mode(self):
        audio_path = "audio_samples/sample_for_pipeline.flac" # (Audio Source: OpenSLR 174-50561-0015.flac)
        output_path = "output/transcript_for_pipeline.txt"

        print("Loading Whisper model...")
        model = whisper.load_model("base")

        print(f"Transcribing: {audio_path}")
        result = model.transcribe(audio_path, fp16=False)

        os.makedirs("output", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print("Transcription result:")
        print(result["text"])
        print(f"Saved to {output_path}")

    def load_selected_model(self):
        print("Select Whisper model size:")
        print("1. tiny       # 39M")
        print("2. base       # 74M")
        print("3. small      # 244M")
        print("4. medium     # 769M")
        print("5. large      # 1550M, highest accuracy")
        print("6. tiny.en    # 39M")
        print("7. base.en    # 74M")
        print("8. small.en   # 244M")
        print("9. medium.en  # 769M")
        print("10. turbo     # 809M, fastest speed")
        model_choices = {
            "1": "tiny", "2": "base", "3": "small", "4": "medium", "5": "large",
            "6": "tiny.en", "7": "base.en", "8": "small.en", "9": "medium.en", "10": "turbo"
        }
        choice = input("Enter 1–10: ").strip()
        model_size = model_choices.get(choice, "base")

        model_dir = os.path.join("models", "whisper")
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, f"{model_size}.pt")

        if os.path.isfile(model_path):
            print(f"Loading cached model from {model_path}...")
        else:
            print(f"Downloading model '{model_size}' to {model_path}...")

        return whisper.load_model(model_size, download_root=model_dir) # load_model() will not re-download the model if it already exists


    def record_audio(self, duration):
        print(f"Recording {duration} seconds...")
        sd.check_input_settings(device=3, channels=1, samplerate=16000, dtype='int16')
        audio = sd.rec(
            int(duration * self.SAMPLE_RATE), 
            samplerate=self.SAMPLE_RATE, 
            channels=1, 
            dtype='int16',
            device=3
            )
        
        sd.wait()
        print("Recording finished.")
        print("First few samples:", audio[:10].flatten())
        if np.all(audio == 0):
            print("Warning: All audio samples are 0 — no sound was recorded.")
        else:
            print("Audio contains non-zero values.")
        return audio

    def save_wav(self, audio_data, filename):
        wav.write(filename, self.SAMPLE_RATE, audio_data)
        print(f"Audio saved to: {filename}")

    def save_transcript(self, text, tag="output"):
        os.makedirs("output", exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_path = os.path.join("output", f"transcript_{tag}_{timestamp}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Transcript saved to: {output_path}")

    def transcribe_audio(self, filename):
        print("Transcribing audio...")
        result = self.model.transcribe(filename, fp16=False)
        print("Transcription:")
        print(result["text"])
        self.save_transcript(result["text"], tag="manual")

    def manual_mode(self):
        try:
            duration = float(input("Enter recording duration in seconds: "))
            if duration <= 0:
                print("Please enter a positive number.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        audio = self.record_audio(duration)

        os.makedirs("audio_samples", exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        audio_path = os.path.join("audio_samples", f"manual_{timestamp}.wav")
        self.save_wav(audio, audio_path)

        self.transcribe_audio(audio_path)
        # with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        #     self.save_wav(audio, tmpfile.name)
        #     audio_path = tmpfile.name

        # self.transcribe_audio(audio_path)
        # os.remove(audio_path)

    def audio_stream(self):
        """
        Starts an audio input stream that continuously records microphone input.
        Captured audio chunks are sent to a queue for real-time transcription.
        """

        def callback(indata, frames, time_info, status):
            """
            This callback is triggered whenever a new audio block is captured.
            It copies the audio data and places it into the queue for processing.
            """
            if status:
                print("Status:", status)
            self.audio_q.put(indata.copy()) # add a block data

        """
        Opens a real-time audio input stream using sounddevice.
        Continuously captures audio in blocks and triggers the callback function.
        """
        with sd.InputStream(
                channels=1,
                blocksize=16000,
                samplerate=self.SAMPLE_RATE,
                dtype='int16',
                callback=callback):
            while True:
                """
                The InputStream runs in non-blocking mode, meaning it records audio in the background and sends data to the callback function.
                The while True: sd.sleep(100) loop keeps the program running, so the stream stays open and continues capturing audio.
                """
                sd.sleep(100)

    def transcribe_stream(self):
        buffer = np.zeros((0, 1), dtype='int16')

        while True:
            chunk = self.audio_q.get() # get a block data
            buffer = np.concatenate((buffer, chunk), axis=0)

            if len(buffer) >= self.CHUNK_SIZE:
                segment = buffer[:self.CHUNK_SIZE]
                head = self.CHUNK_SIZE * (1 - self.OVERLAP)
                buffer = buffer[head:]
                # buffer = buffer[int(self.CHUNK_SIZE * self.OVERLAP):]

                # Save audio segment
                # os.makedirs("audio_samples", exist_ok=True)
                # timestamp = time.strftime("%Y%m%d-%H%M%S")
                # audio_path = os.path.join("audio_samples", f"stream_{timestamp}.wav")
                # wav.write(audio_path, self.SAMPLE_RATE, segment)

                # Make transcribe 
                audio = segment.astype(np.float32) / 32768.0  # 轉換為 [-1.0, 1.0] 的 float32
                audio = audio.flatten()  # 去掉多維度 (如果是 (16000,1))
                result = self.model.transcribe(audio, fp16=False)
                # result = self.model.transcribe(audio_path, fp16=False)
                new_text = result["text"]

                # Remove duplicate prefix if any
                # if new_text.startswith(self.last_text):
                #     new_text = new_text[len(self.last_text):].lstrip()
                # self.last_text = new_text

                # print(">>", result["text"])
                print(">>", new_text)
                self.transcripts.append(new_text)

    def streaming_mode(self):
        print("Starting real-time transcription (Ctrl+C to stop)...")
        threading.Thread(target=self.audio_stream, daemon=True).start()
        threading.Thread(target=self.transcribe_stream, daemon=True).start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopped by user.")
            if self.transcripts:
                full_text = "\n".join(self.transcripts)
                self.save_transcript(full_text, tag="stream")
