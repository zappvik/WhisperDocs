# Whisper Docs

Whisper Docs is a desktop application that converts PDF documents to audio files. The app includes a simple login interface, PDF upload, conversion to audio, and playback functionality with a progress indicator.

## Features
- **History**: Basic history interface to view past recordings.
- **PDF Upload**: Allows users to upload PDF files for conversion.
- **Convert to Audio**: Converts the uploaded PDF to an audio file.
- **Audio Playback**: Plays the converted audio file within the app.
- **Progress Display**: Shows audio playback progress.

## Requirements
- **Python** 3.6 or higher
- **Required Packages**:
  - **Pygame** (install using `pip install pygame`)
  - **pdfminer** (install using `pip install pdfminer.six`)
  - **Google Text-To-Speech** (install using `pip install gTTS`)

## Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/codebylohit/Whisper_Docs
   cd Whisper_Docs

## Usage
1. Run the application: 
    ```bash
    python program.py

2. **Upload a PDF** by clicking the `upload PDF` button.

3. **Convert to audio** by clicking the `Convert PDF to Audio` button.
4. **Play Audio** using the `Play Audio` button, which will also display the playback progress.
