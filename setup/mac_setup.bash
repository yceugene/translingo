# Create conda environment
conda create -n translingo python=3.9
conda activate translingo

# Install scientific libraries using conda (faster and more stable)
conda install numpy scipy

# Install other Python packages using pip
pip install sounddevice
pip install git+https://github.com/openai/whisper.git

# Install ffmpeg (required for audio processing)
brew install ffmpeg

# For GoogleRecognizer (speech_recognition with Microphone support)
brew install portaudio
pip install pyaudio
pip install SpeechRecognition