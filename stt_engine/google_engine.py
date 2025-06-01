### translingo/stt_engine/google_engine.py
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import time
import tempfile

class GoogleRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language_codes = {
            "1": ("Romanian", "ro-RO"),
            "2": ("English", "en-US"),
            "3": ("Malayalam", "ml-IN"),
            "4": ("Telugu", "te-IN"),
            "5": ("Spanish", "es-ES"),
            "6": ("Mandarin", "zh-CN")
        }
        self.language_name, self.lang_code = self.select_language()

    def select_language(self):
        print("Choose a language for speech recognition:")
        for key, (lang, _) in self.language_codes.items():
            print(f"{key}. {lang}")
        choice = input("Enter your choice (1–6): ").strip()
        return self.language_codes.get(choice, ("English", "en-US"))
    
    def save_transcript(self, text, language_name):
        os.makedirs("output", exist_ok=True)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_path = os.path.join("output", f"transcript_google_{language_name}_{timestamp}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Transcript saved to: {output_path}")

    def manual_mode(self):
        print(f"\nManual recording in {self.language_name} ({self.lang_code})")
        try:
            duration = float(input("Enter duration (seconds): "))
            if duration <= 0:
                print("Please enter a positive number.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        # Record using sounddevice
        SAMPLE_RATE = 16000
        print("Recording...")
        audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
        sd.wait()
        print("Recording finished.")

        # Save as temporary wav
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            wav.write(tmpfile.name, SAMPLE_RATE, audio)
            temp_path = tmpfile.name

        try:
            with sr.AudioFile(temp_path) as source:
                audio_data = self.recognizer.record(source)
                print("Transcribing...")
                text = self.recognizer.recognize_google(audio_data, language=self.lang_code)
                print(f"{self.language_name}: {text}")
                self.save_transcript(text, self.language_name.replace(" ", "_"))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            os.remove(temp_path)

    # def manual_mode(self):
    #     print(f"\nManual recording in {self.language_name} ({self.lang_code})")
    #     try:
    #         with sr.Microphone() as source:
    #             self.recognizer.adjust_for_ambient_noise(source)
    #             duration = float(input("Enter duration (seconds): "))
    #             print("Recording...")
    #             audio = self.recognizer.record(source, duration=duration)
    #             print("Transcribing...")
    #             text = self.recognizer.recognize_google(audio, language=self.lang_code)
    #             print(f"{self.language_name}: {text}")
    #             self.save_transcript(text, self.language_name.replace(" ", "_"))
    #     except Exception as e:
    #         print(f"Error: {e}")

    def streaming_mode(self):
        print(f"\nStreaming recognition in {self.language_name} ({self.lang_code})... Press Ctrl+C to stop.")
        transcripts = []
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                while True:
                    print("Speak now...")
                    audio = self.recognizer.listen(source, phrase_time_limit=15)
                    try:
                        text = self.recognizer.recognize_google(audio, language=self.lang_code)
                        print(f"{self.language_name}: {text}")
                        transcripts.append(text)
                    except sr.UnknownValueError:
                        print("Could not understand audio.")
                    except sr.RequestError:
                        print("API unavailable or quota exceeded.")
        except KeyboardInterrupt:
            print("\nStopped by user.")
            if transcripts:
                full_text = "\n".join(transcripts)
                self.save_transcript(full_text, self.language_name.replace(" ", "_"))


    # def streaming_mode(self):
    #     print(f"\nStreaming recognition in {self.language_name} ({self.lang_code})... Press Ctrl+C to stop.")
    #     transcripts = []
    #     try:
    #         with sr.Microphone() as source:
    #             self.recognizer.adjust_for_ambient_noise(source)
    #             while True:
    #                 print("Speak now...")
    #                 audio = self.recognizer.listen(source, phrase_time_limit=15)
    #                 try:
    #                     text = self.recognizer.recognize_google(audio, language=self.lang_code)
    #                     print(f"{self.language_name}: {text}")
    #                     transcripts.append(text)
    #                 except sr.UnknownValueError:
    #                     print("Could not understand audio.")
    #                 except sr.RequestError:
    #                     print("API unavailable or quota exceeded.")
    #     except KeyboardInterrupt:
    #         print("\nStopped by user.")
    #         if transcripts:
    #             full_text = "\n".join(transcripts)
    #             self.save_transcript(full_text, self.language_name.replace(" ", "_"))


    # def run(self):
    #     print("Choose a language for speech recognition:")
    #     for key, (lang, _) in self.language_codes.items():
    #         print(f"{key}. {lang}")

    #     choice = input("Enter your choice (1–6): ").strip()
    #     language_name, lang_code = self.language_codes.get(choice, ("English", "en-US"))

    #     print(f"\nListening continuously in {language_name} ({lang_code})... Press Ctrl+C to stop.")

    #     transcripts = []

    #     try:
    #         with sr.Microphone() as source:
    #             self.recognizer.adjust_for_ambient_noise(source)
    #             while True:
    #                 print("Speak now...")
    #                 audio = self.recognizer.listen(source, phrase_time_limit=15)
    #                 try:
    #                     text = self.recognizer.recognize_google(audio, language=lang_code)
    #                     print(f"{language_name}: {text}")
    #                 except sr.UnknownValueError:
    #                     print("Could not understand audio.")
    #                 except sr.RequestError:
    #                     print("API unavailable or quota exceeded.")
    #     except KeyboardInterrupt:
    #         print("\nStopped by user.")
    #         if transcripts:
    #             full_text = "\n".join(transcripts)
    #             self.save_transcript(full_text, language_name.replace(" ", "_"))
