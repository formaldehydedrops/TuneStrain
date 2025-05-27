# TuneStrain

Пакетный конвертер видео в mp3 с красивым GUI на PyQt6

## Для пользователей

- Просто скачайте установщик (TuneStrainSetup.exe) из [релизов](https://github.com/yourusername/TuneStrain/releases) и установите.
- После установки можно запускать TuneStrain из меню Пуск или ярлыка на рабочем столе.
- **FFmpeg уже встроен** — ничего дополнительно устанавливать не нужно.

## Для разработчиков

### Быстрый старт

1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/yourusername/TuneStrain.git
   cd TuneStrain
   ```
2. Установите зависимости:
   ```sh
   pip install -r requirements.txt
   ```
3. Убедитесь, что у вас установлен ffmpeg (или положите ffmpeg.exe рядом с main.py).
4. Запустите:
   ```sh
   python main.py
   ```

### Сборка exe

1. Установите PyInstaller:
   ```sh
   pip install pyinstaller
   ```
2. Соберите exe:
   ```sh
   pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data "assets;assets" --add-data "style.qss;." --add-data "converter_module.py;." --hidden-import=moviepy --hidden-import=pydub main.py
   ```
3. Положите ffmpeg.exe и ffprobe.exe в папку dist рядом с exe.

### Сборка установщика (Inno Setup)

1. Переименуйте main.exe → TuneStrain.exe (опционально).
2. Используйте такой скрипт для Inno Setup:

```iss
[Setup]
AppName=TuneStrain
AppVersion=1.0
DefaultDirName={pf}\TuneStrain
DefaultGroupName=TuneStrain
UninstallDisplayIcon={app}\TuneStrain.exe
OutputBaseFilename=TuneStrainSetup
SetupIconFile=assets\icon.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\\TuneStrain.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\\ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\\ffprobe.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\\style.qss"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\\*"; DestDir: "{app}\\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "converted\\*"; DestDir: "{app}\\converted"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "output\\*"; DestDir: "{app}\\output"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\TuneStrain"; Filename: "{app}\\TuneStrain.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\\TuneStrain.exe"; Description: "Запустить TuneStrain"; Flags: nowait postinstall skipifsilent
```

---

## Структура проекта
- `main.py` — основной GUI
- `converter_module.py` — функции конвертации
- `assets/` — иконки, шрифты, ffmpeg (если нужно)
- `style.qss` — стили для тёмной темы
- `requirements.txt` — зависимости для разработки

---

**Вопросы и баги** — пишите в Issues на GitHub!
