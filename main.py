from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QProgressBar, QTextEdit, QSizePolicy, QMessageBox, QComboBox, QHBoxLayout
)
from PyQt6.QtGui import QFontDatabase, QFont, QIcon
from PyQt6.QtCore import Qt, QTimer, QSettings
import sys, os, subprocess
from converter_module import convert_mp4_to_mp3
import moviepy

def add_ffmpeg_to_path():
    exe_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.argv[0])))
    if os.path.exists(os.path.join(exe_dir, "ffmpeg.exe")):
        os.environ["PATH"] = exe_dir + os.pathsep + os.environ["PATH"]

add_ffmpeg_to_path()

class TuneStrainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TuneStrain")
        self.setWindowIcon(QIcon("assets/icon.ico"))
        self.setAcceptDrops(True)
        self.setFixedSize(600, 500)

        # QSettings для сохранения настроек
        self.settings = QSettings("TuneStrain", "TuneStrainApp")

        # Подключаем шрифты Montserrat через абсолютный путь
        font_dir = os.path.join(os.path.dirname(__file__), "assets", "fonts")
        QFontDatabase.addApplicationFont(os.path.join(font_dir, "Montserrat-Regular.ttf"))
        QFontDatabase.addApplicationFont(os.path.join(font_dir, "Montserrat-Bold.ttf"))

        # Темы
        self.light_qss = """
            QWidget {
                background-color: #f5f5fa;
                color: #1e1b2e;
                font-family: 'Montserrat';
                font-size: 14px;
            }
            QLabel#TitleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #7c3aed;
            }
            QLabel#FooterLabel {
                color: #bdbdbd;
                font-size: 10px;
            }
            QPushButton {
                background-color: #7c3aed;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-family: 'Montserrat';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a78bfa;
            }
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background-color: #f0f0f0;
                text-align: center;
                color: #1e1b2e;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #7c3aed;
            }
            QTextEdit {
                background-color: #f0f0f0;
                border: none;
                padding: 10px;
                font-family: 'Montserrat';
            }
            QWidget[dragActive="true"] {
                border: 2px dashed #7c3aed;
            }
        """
        self.dark_qss = open("style.qss", encoding="utf-8").read() if os.path.exists("style.qss") else self.styleSheet()
        self.theme = self.settings.value("theme", "dark")
        self.apply_theme(self.theme)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Header
        self.title = QLabel("TuneStrain")
        self.title.setObjectName("TitleLabel")
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)

        # File Info
        self.file_info = QLabel("Drop or choose video files/folders to convert")
        self.file_info.setWordWrap(True)
        self.file_info.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.file_info.setMinimumWidth(500)
        self.file_info.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.file_info)

        # Кнопки действий (Choose, Convert, Очистить, Открыть папку)
        btns_layout = QHBoxLayout()
        self.action_btn = QPushButton("Choose files/folders")
        self.action_btn.clicked.connect(self.choose_files)
        btns_layout.addWidget(self.action_btn)
        self.clear_btn = QPushButton("Clear list")
        self.clear_btn.clicked.connect(self.clear_files)
        btns_layout.addWidget(self.clear_btn)
        self.open_folder_btn = QPushButton("Open output folder")
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        btns_layout.addWidget(self.open_folder_btn)
        self.layout.addLayout(btns_layout)

        # Прогресс-бар
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.layout.addWidget(self.progress)

        # Log Area
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.layout.addWidget(self.log)

        # Output Folder Selector
        self.output_dir = self.settings.value("output_dir", os.path.join(os.getcwd(), "converted"))
        self.output_dir_label = QLabel(f"Output folder: {self.output_dir}")
        self.output_dir_label.setStyleSheet("color: #a78bfa; font-size: 12px;")
        self.layout.addWidget(self.output_dir_label)
        self.choose_output_btn = QPushButton("Choose output folder")
        self.choose_output_btn.clicked.connect(self.choose_output_folder)
        self.layout.addWidget(self.choose_output_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Настройка битрейта
        bitrate_layout = QHBoxLayout()
        self.bitrate_label = QLabel("MP3 bitrate:")
        bitrate_layout.addWidget(self.bitrate_label)
        self.bitrate_combo = QComboBox()
        self.bitrate_combo.addItems(["128k", "192k", "256k", "320k"])
        saved_bitrate = self.settings.value("bitrate", "192k")
        idx = self.bitrate_combo.findText(saved_bitrate)
        if idx >= 0:
            self.bitrate_combo.setCurrentIndex(idx)
        bitrate_layout.addWidget(self.bitrate_combo)
        self.layout.addLayout(bitrate_layout)

        # Переключатель темы
        self.theme_btn = QPushButton("Switch theme")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_btn, alignment=Qt.AlignmentFlag.AlignRight)

        # Footer
        self.footer = QLabel("@formaldehydedrops")
        self.footer.setObjectName("FooterLabel")
        self.layout.addWidget(self.footer, alignment=Qt.AlignmentFlag.AlignRight)

        self.selected_files = []
        self.is_ready_to_convert = False

        # Проверка ffmpeg
        self.check_ffmpeg()

    def apply_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet(self.dark_qss)
        else:
            self.setStyleSheet(self.light_qss)
        self.theme = theme
        self.settings.setValue("theme", theme)

    def toggle_theme(self):
        new_theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme(new_theme)

    def check_ffmpeg(self):
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception()
        except Exception:
            QMessageBox.warning(self, "FFmpeg not found", "FFmpeg is not installed or not in PATH! Conversion will not work.")

    def choose_files(self):
        file_dialog = QFileDialog()
        video_exts = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm')
        files, _ = file_dialog.getOpenFileNames(self, "Select Video Files", "", "Video Files (*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm)")
        if not files:
            # Попробуем выбрать папку
            folder = QFileDialog.getExistingDirectory(self, "Select Folder with Videos", "")
            if folder:
                files = self.get_videos_from_folder(folder, video_exts)
        if files:
            self.selected_files = self.unique_files(self.selected_files + files)
            self.is_ready_to_convert = True
            self.action_btn.setText("Convert to MP3")
            self.action_btn.clicked.disconnect()
            self.action_btn.clicked.connect(self.convert_files)
            self.file_info.setText(f"Selected {len(self.selected_files)} file(s):")
            self.log.clear()
            for f in self.selected_files:
                self.log.append(f"• {os.path.basename(f)}")
        else:
            self.selected_files = []
            self.is_ready_to_convert = False
            self.file_info.setText("Drop or choose video files/folders to convert")
            self.log.clear()
            self.action_btn.setText("Choose files/folders")
            self.action_btn.clicked.disconnect()
            self.action_btn.clicked.connect(self.choose_files)

    def clear_files(self):
        self.selected_files = []
        self.is_ready_to_convert = False
        self.file_info.setText("Drop or choose video files/folders to convert")
        self.log.clear()
        self.action_btn.setText("Choose files/folders")
        self.action_btn.clicked.disconnect()
        self.action_btn.clicked.connect(self.choose_files)

    def open_output_folder(self):
        path = os.path.realpath(self.output_dir)
        if os.name == 'nt':
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def choose_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", self.output_dir)
        if folder:
            self.output_dir = folder
            self.output_dir_label.setText(f"Output folder: {self.output_dir}")
            self.settings.setValue("output_dir", self.output_dir)

    def convert_files(self):
        if not self.selected_files:
            self.file_info.setText("No files selected!")
            return
        self.progress.setValue(0)
        self.file_info.setText(f"Converting {len(self.selected_files)} file(s)...")
        self.log.append("\n--- Conversion started ---\n")
        total = len(self.selected_files)
        converted = 0
        errors = 0
        bitrate = self.bitrate_combo.currentText()
        self.settings.setValue("bitrate", bitrate)
        for idx, file_path in enumerate(self.selected_files):
            try:
                output_path = convert_mp4_to_mp3(file_path, self.output_dir, bitrate=bitrate)
                self.log.append(f"[✔] {os.path.basename(file_path)} → {os.path.basename(output_path)}")
                converted += 1
            except Exception as e:
                self.log.append(f"[✖] {os.path.basename(file_path)}: {e}")
                errors += 1
            self.progress.setValue(int((idx + 1) / total * 100))
            self.log.append(f"Progress: {idx+1}/{total}")
            QApplication.processEvents()
        self.file_info.setText(f"✅ Done! Converted: {converted}, Errors: {errors}")
        QMessageBox.information(self, "Conversion finished", f"Done! Converted: {converted}, Errors: {errors}")
        self.action_btn.setText("Choose files/folders")
        self.action_btn.clicked.disconnect()
        self.action_btn.clicked.connect(self.choose_files)
        self.selected_files = []
        self.is_ready_to_convert = False

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragActive", True)
            self.setStyle(self.style())

    def dragLeaveEvent(self, event):
        self.setProperty("dragActive", False)
        self.setStyle(self.style())

    def dropEvent(self, event):
        self.setProperty("dragActive", False)
        self.setStyle(self.style())
        urls = event.mimeData().urls()
        video_exts = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm')
        files = []
        for url in urls:
            file_path = url.toLocalFile()
            if os.path.isdir(file_path):
                files += self.get_videos_from_folder(file_path, video_exts)
            elif os.path.isfile(file_path) and file_path.lower().endswith(video_exts):
                files.append(file_path)
        all_files = self.unique_files(self.selected_files + files)
        if all_files:
            self.selected_files = all_files
            self.is_ready_to_convert = True
            self.action_btn.setText("Convert to MP3")
            self.action_btn.clicked.disconnect()
            self.action_btn.clicked.connect(self.convert_files)
            self.file_info.setText(f"Selected {len(all_files)} file(s):")
            self.log.clear()
            for f in all_files:
                self.log.append(f"• {os.path.basename(f)}")
        else:
            self.selected_files = []
            self.is_ready_to_convert = False
            self.file_info.setText("Drop or choose video files/folders to convert")
            self.log.clear()
            self.action_btn.setText("Choose files/folders")
            self.action_btn.clicked.disconnect()
            self.action_btn.clicked.connect(self.choose_files)

    def get_videos_from_folder(self, folder, video_exts):
        result = []
        for root, _, files in os.walk(folder):
            for f in files:
                if f.lower().endswith(video_exts):
                    result.append(os.path.join(root, f))
        return result

    def unique_files(self, files):
        seen = set()
        unique = []
        for f in files:
            if f not in seen:
                unique.append(f)
                seen.add(f)
        return unique

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TuneStrainUI()
    window.show()
    sys.exit(app.exec())
