# Translingo

Translingo is a real-time, multilingual speech-to-text application that uses concepts and tools from OpenAI's Whisper.


## Features
- Speech-to-text (STT) from audio files or microphone input
- Multilingual support (e.g., English, Chinese, Spanish, French, etc.)
- Speech translation to English
- Language identification
- CLI and Gradio web interface (planned)
- Offline model loading (no internet needed after setup)
---

## Getting Started
### 1. Clone the Repository

```bash
git clone https://github.com/yceugene/translingo.git
cd translingo
```

### 2. Create Python environment
``` bash
conda create -n translingo python=3.9.9
conda activate translingo

# To activate this environment, use $ conda activate translingo
# To deactivate an active environment, use $ conda deactivate
```

### 3. Install Dependencies (Mac OS)
- If you're on Apple Silicon (M1/M2), make sure PyTorch supports MPS and disable fp16 in transcription.
``` bash 

# Install core scientific libraries (via conda for stability)
conda install numpy scipy

# Install Whisper and audio libraries
pip install sounddevice
pip install git+https://github.com/openai/whisper.git

# Install ffmpeg (required for audio processing)
brew install ffmpeg

# Install GoogleRecognizer dependencies
brew install portaudio
pip install pyaudio
pip install SpeechRecognition
```

### 4. Run the program
1. Run main.py
``` bash
% python main.py
```

2. Select mode
``` bash
Select mode:
1. Manual recording with fixed duration (Whisper)
2. Real-time streaming with simulated subtitle effect (Whisper)
3. Manual recording with fixed duration (Google API)
4. Real-time streaming (Google API)
```

#### Modes Explained:
1. Manual recording with fixed duration (Whisper):
Record a fixed-length audio clip via microphone and transcribe it using OpenAI's Whisper model.

2. Real-time streaming with simulated subtitle effect (Whisper):
Continuously capture microphone input and display live transcription using Whisper.

3. Manual recording with fixed duration (Google API):
Record a fixed-length audio sample and transcribe it using Google Speech Recognition.

4. Real-time streaming (Google API):
Continuously stream audio input from microphone and transcribe it in real time using Google API.

**Note**:

- For mode 1 and 2, ensure you are connected to the internet the first time you use each Whisper model (the model will be downloaded).

- For mode 3 and 4, ensure you are connected to the internet every time (Google API is cloud-based).


## Project Structure
``` bash
translingo/
├── main.py                 # Entry point (CLI)
├── README.md               # This file
├── requirements.txt        # Required packages
├── docs/
│   └── setup.md            # Environment setup instructions
│
├── stt_engine/             # Speech engine implementations
│   ├── base.py             # Abstract interface
│   ├── whisper_engine.py   # Whisper implementation
│   └── google_engine.py    # Google STT (Optional)
│
├── app/                    # App interfaces (Todo)
│   ├── cli_runner.py       # CLI interface (Todo)
│   └── ui_gradio.py        # Gradio Web UI (WIP) (Todo)
│
├── audio_samples/          # Test audio files
│   └── sample.wav
├── output/                 # Transcription output files
│   └── transcript.txt
└── utils/                  # Utilities (e.g., WER) (Todo)
    └── metrics.py          # (Todo)

```

## Models
By default, the Whisper model is downloaded and cached locally on first use.
To preload manually and run offline:
``` python
import whisper
model = whisper.load_model("base")
result = model.transcribe("sample.wav", fp16=False)  # Use fp16=False on M1/M2
print(result["text"])
```

## Todo list
- app/                     # App interfaces
- utils/                   # Utilities (e.g., WER)

## License
MIT for code. Whisper model weights are subject to OpenAI’s terms of use.