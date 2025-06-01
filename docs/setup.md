## Setup Instructions for translingo

These are the recommended steps to set up a clean development environment using conda and pip.


### Create Environment
```bash
conda create -n translingo python=3.9
conda activate translingo
```

### Install System Tools
```bash
# Install ffmpeg (required for audio processing)
brew install ffmpeg  # for macOS

# For GoogleRecognizer (speech_recognition with Microphone support)
brew install portaudio
```

### Install Dependencies
```bash
# Install scientific libraries using conda (faster and more stable)
conda install numpy scipy

# Install other Python packages using pip
pip install sounddevice
pip install git+https://github.com/openai/whisper.git

pip install pyaudio
pip install SpeechRecognition
```


### Export Environment
```bash
conda env export --from-history > env_base.yml
conda env export > full_env.yml
```

You can share env_base.yml or full_env.yml with collaborators to recreate the environment.


### Project Structure
```
translingo/
├── main.py                 # Entry point (CLI)
├── README.md               # Project overview
├── requirements.txt        # Required pip packages
├── docs/
│   └── setup.md            # Environment setup instructions
│
├── stt_engine/             # Speech engine implementations
│   ├── base.py             # Abstract interface
│   ├── whisper_engine.py   # Whisper implementation
│   └── google_engine.py    # Google STT (Optional)
│
├── app/                    # App interfaces
│   ├── cli_runner.py       # CLI interface
│   └── ui_gradio.py        # Web UI (WIP)
│
├── audio_samples/          # Test audio files
│   └── sample.wav
├── output/                 # Transcription output files
│   └── transcript.txt
└── utils/                  # Utilities (e.g., WER)
    └── metrics.py
```
