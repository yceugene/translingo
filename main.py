### translingo/main.py
import sys
from stt_engine.whisper_engine import WhisperRecognizer
from stt_engine.google_engine import GoogleRecognizer

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--pipeline":
        print("=== Pipeline Mode Start ===")
        # Whisper
        recognizer = WhisperRecognizer(isPipeline=True)
        recognizer.run_pipeline_mode()

        # Google
        gooRecognizer = GoogleRecognizer(isPipeline=True)
        gooRecognizer.run_pipeline_mode()
        print("=== Pipeline Mode Complete ===")
        return

    print("Select mode:")
    print("1. Manual recording with fixed duration (Whisper)")
    print("2. Real-time streaming with simulated subtitle effect (Whisper)")
    print("3. Manual recording with fixed duration (Google API)")
    print("4. Real-time streaming (Google API)")
    print("5. Test")
    choice = input("Enter 1-4: ")

    if choice == "1":
        whiRecognizer = WhisperRecognizer()
        whiRecognizer.manual_mode()
    elif choice == "2": # Real-time streaming
        whiRecognizer = WhisperRecognizer()
        whiRecognizer.streaming_mode()
    elif choice == "3":
        gooRecognizer = GoogleRecognizer()
        gooRecognizer.manual_mode()
    elif choice == "4":
        gooRecognizer = GoogleRecognizer()
        gooRecognizer.streaming_mode()
    elif choice == "5":
        whiRecognizer = WhisperRecognizer()
        whiRecognizer.test_input_devices()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
