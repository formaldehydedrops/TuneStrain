# TuneStrain

Batch video to mp3 converter with a modern PyQt6 GUI

## For users

- Download the installer (`TuneStrainSetup.exe`) from [Releases](https://github.com/yourusername/TuneStrain/releases) and install.
- After installation, run TuneStrain from the Start menu or desktop shortcut.
- **FFmpeg is built-in** — no extra installation required.

## For developers

### Quick start

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/TuneStrain.git
   cd TuneStrain
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Make sure you have ffmpeg in your PATH or place `ffmpeg.exe` next to `main.py`.

4. Run:

   ```sh
   python main.py
   ```

### Build exe

1. Install PyInstaller:

   ```sh
   pip install pyinstaller
   ```

2. Build the executable:

   ```sh
   pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data "assets;assets" --add-data "style.qss;." --add-data "fonts;fonts" --hidden-import=moviepy --hidden-import=pydub main.py --name TuneStrain
   ```

3. Place `ffmpeg.exe` and `ffprobe.exe` in the `dist` folder next to the exe.

### Build the installer (Inno Setup)

1. Open `TuneStrain.iss` in Inno Setup Compiler.
2. Build the installer. The script will include all required resources.

---

## Project structure

- `main.py` — main GUI
- `converter_module.py` — conversion logic
- `assets/` — icons
- `fonts/` — fonts
- `style.qss` — dark theme styles
- `TuneStrain.iss` — Inno Setup script
- `requirements.txt` — Python dependencies

---

**Questions and Bugs:** Please use GitHub Issues!
