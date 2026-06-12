import sys
import os
import warnings
import re
import logging
import base64
import hashlib
from datetime import datetime

# ffmpeg uyarısını sustur
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub")

# --- LOGGING ---
log_filename = "markitdown_gui.log"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_filename, encoding='utf-8'), logging.StreamHandler(sys.stdout)])

# --- FFmpeg CONFIG ---
def configure_ffmpeg():
    winget_ffmpeg = r"C:\Users\tcoerman\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin"
    if os.path.exists(winget_ffmpeg):
        os.environ["PATH"] += os.pathsep + winget_ffmpeg
        try:
            from pydub import AudioSegment
            AudioSegment.converter = os.path.join(winget_ffmpeg, "ffmpeg.exe")
            logging.info(f"FFmpeg configured: {winget_ffmpeg}")
        except: pass

configure_ffmpeg()

# --- SILENCER ---
class SilenceStdout:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

with SilenceStdout():
    from qfluentwidgets import (
        TitleLabel, SubtitleLabel, PrimaryPushButton, CardWidget, 
        ProgressBar, InfoBar, InfoBarPosition, ComboBox, 
        setTheme, Theme, setThemeColor, StrongBodyLabel, IconWidget,
        BodyLabel, TextEdit, TransparentPushButton, ImageLabel, Flyout, FlyoutView, FlyoutAnimationType
    )
    from qfluentwidgets import FluentIcon as FIF

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QLocale, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QColor, QFont, QIcon, QDesktopServices
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QFileDialog, QWidget, QMainWindow, QLabel
from markitdown import MarkItDown

# --- APP CONFIG ---
GITHUB_URL = "https://github.com/omererman/markitdown-desktop"
DEVELOPER_NAME = "OMER ERMAN"
VERSION = "v1.0.0"

TRANSLATIONS = {
    "English": {
        "title": "MarkItDown", "subtitle": "Convert complex documents to Markdown", "drop_text": "Select a File or Drag & Drop Here", "success_title": "Success", "success_msg": "File saved: ", "error_title": "Error", "error_msg": "An error occurred: ", "select_file": "Select File", "logs": "Action Logs", "auto_detect": "System language: English", "about_title": "About This App", "about_dev": "Developed by", "about_desc": "A professional tool for high-fidelity document conversion.", "about_tech": "Built with Microsoft MarkItDown & PyQt6"
    },
    "Türkçe": {
        "title": "MarkItDown", "subtitle": "Karmaşık belgeleri MD'ye dönüştürün", "drop_text": "Bir Dosya Seçin veya Üzerine Sürükleyin", "success_title": "İşlem Başarılı", "success_msg": "Dosya kaydedildi: ", "error_title": "Hata", "error_msg": "Bir hata oluştu: ", "select_file": "Dosya Seç", "logs": "İşlem Kayıtları", "auto_detect": "Sistem dili: Türkçe", "about_title": "Uygulama Hakkında", "about_dev": "Geliştiren", "about_desc": "Yüksek kaliteli döküman dönüşümü için profesyonel araç.", "about_tech": "Microsoft MarkItDown & PyQt6 ile hazırlandı"
    },
    "Español": {
        "title": "MarkItDown", "subtitle": "Convertir documentos complejos a Markdown", "drop_text": "Seleccione un archivo o arrástrelo aquí", "success_title": "Éxito", "success_msg": "Archivo guardado: ", "error_title": "Error", "error_msg": "Ocurrió un error: ", "select_file": "Seleccionar archivo", "logs": "Registros de acción", "auto_detect": "Idioma del sistema: Español", "about_title": "Sobre esta aplicación", "about_dev": "Desarrollado por", "about_desc": "Herramienta profesional para la conversión de documentos.", "about_tech": "Construido con MarkItDown y PyQt6"
    },
    "Français": {
        "title": "MarkItDown", "subtitle": "Convertir des documents complexes en Markdown", "drop_text": "Sélectionnez un fichier ou glissez-le ici", "success_title": "Succès", "success_msg": "Fichier enregistré : ", "error_title": "Erreur", "error_msg": "Une erreur est survenue : ", "select_file": "Choisir un fichier", "logs": "Journaux d'action", "auto_detect": "Langue du système : Français", "about_title": "À propos", "about_dev": "Développé par", "about_desc": "Outil professionnel de conversion de documents.", "about_tech": "Construit avec MarkItDown et PyQt6"
    },
    "Deutsch": {
        "title": "MarkItDown", "subtitle": "Komplexe Dokumente in Markdown konvertieren", "drop_text": "Datei auswählen oder hierher ziehen", "success_title": "Erfolg", "success_msg": "Datei gespeichert: ", "error_title": "Fehler", "error_msg": "Ein Fehler ist aufgetreten: ", "select_file": "Datei auswählen", "logs": "Aktionsprotokolle", "auto_detect": "Systemsprache: Deutsch", "about_title": "Über diese App", "about_dev": "Entwickelt von", "about_desc": "Professionelles Werkzeug zur Dokumentkonvertierung.", "about_tech": "Erstellt mit MarkItDown und PyQt6"
    },
    "中文": {
        "title": "MarkItDown", "subtitle": "将复杂文档转换为 Markdown", "drop_text": "选择文件或拖放到此处", "success_title": "成功", "success_msg": "文件已保存：", "error_title": "错误", "error_msg": "发生错误：", "select_file": "选择文件", "logs": "操作日志", "auto_detect": "系统语言：中文", "about_title": "关于此应用", "about_dev": "开发者", "about_desc": "专业的高保真文档转换工具。", "about_tech": "基于 Microsoft MarkItDown 和 PyQt6"
    }
}

class MarkItDownWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    def run(self):
        try:
            md = MarkItDown()
            result = md.convert(self.file_path)
            out = f"{os.path.splitext(self.file_path)[0]}.md"
            with open(out, "w", encoding="utf-8") as f: 
                f.write(result.text_content)
            self.finished.emit(out)
        except Exception as e:
            self.error.emit(str(e))

class MarkItDownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarkItDown Desktop")
        self.resize(650, 850)
        
        # LOGO PATH FIX
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.logo_path = os.path.join(curr_dir, "logo.png")
        # Ikinci ihtimal (Eger gui klasoru icinden calisma sorunu varsa)
        if not os.path.exists(self.logo_path):
             self.logo_path = os.path.join(curr_dir, "gui", "logo.png")
        
        if os.path.exists(self.logo_path):
            self.setWindowIcon(QIcon(self.logo_path))
        
        setTheme(Theme.DARK)
        setThemeColor("#0078d4")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(15)

        # Header
        header = QHBoxLayout()
        if os.path.exists(self.logo_path):
            self.logo_label = QLabel()
            self.logo_label.setPixmap(QIcon(self.logo_path).pixmap(40, 40))
            header.addWidget(self.logo_label)
        
        self.title_label = TitleLabel("MarkItDown")
        self.title_label.setTextColor(QColor(255, 255, 255))
        header.addWidget(self.title_label)
        
        header.addStretch(1)
        self.info_btn = TransparentPushButton(FIF.INFO, "", self)
        self.info_btn.clicked.connect(self.showAbout)
        header.addWidget(self.info_btn)
        
        self.lang_box = ComboBox()
        self.lang_box.addItems(list(TRANSLATIONS.keys()))
        header.addWidget(self.lang_box)
        self.layout.addLayout(header)

        self.sub_label = BodyLabel("")
        self.sub_label.setTextColor(QColor(180, 180, 180))
        self.layout.addWidget(self.sub_label)
        self.layout.addSpacing(30)

        self.drop_card = CardWidget()
        self.drop_card.setStyleSheet("CardWidget { border: 2px dashed rgba(255,255,255,0.15); border-radius: 12px; } CardWidget:hover { border: 2px dashed #0078d4; background-color: rgba(0,120,212,0.05); }")
        self.drop_layout = QVBoxLayout(self.drop_card)
        self.drop_layout.setContentsMargins(20, 40, 20, 40)
        self.icon_widget = IconWidget(FIF.DOCUMENT)
        self.icon_widget.setFixedSize(100, 100)
        self.drop_layout.addWidget(self.icon_widget, 0, Qt.AlignmentFlag.AlignCenter)
        self.info_label = StrongBodyLabel("")
        self.info_label.setTextColor(QColor(255, 255, 255))
        self.drop_layout.addWidget(self.info_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.btn = PrimaryPushButton(FIF.FOLDER, "")
        self.btn.setFixedWidth(200)
        self.drop_layout.addWidget(self.btn, 0, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.drop_card)

        self.pbar = ProgressBar()
        self.pbar.setVisible(False)
        self.layout.addWidget(self.pbar)

        self.layout.addSpacing(20)
        log_header = QHBoxLayout()
        self.log_header_label = StrongBodyLabel("")
        self.log_header_label.setTextColor(QColor(150, 150, 150))
        log_header.addWidget(self.log_header_label)
        log_header.addStretch(1)
        self.clear_btn = TransparentPushButton(FIF.DELETE, "", self)
        self.clear_btn.clicked.connect(lambda: self.log_area.clear())
        log_header.addWidget(self.clear_btn)
        self.layout.addLayout(log_header)

        self.log_area = TextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(180)
        self.log_area.setStyleSheet("TextEdit { background-color: #121212; border: 1px solid #333; color: #aaa; font-family: 'Consolas'; }")
        self.layout.addWidget(self.log_area)
        self.setStyleSheet("QMainWindow { background-color: #101010; }")

        self.detectLanguage()
        self.lang_box.currentTextChanged.connect(self.updateLang)
        self.btn.clicked.connect(self.selectFile)
        self.setAcceptDrops(True)

    def showAbout(self):
        t = TRANSLATIONS[self.lang_key]
        spec_text = "Supported Formats:\n• Documents: PDF, DOCX, XLSX, PPTX\n• Data & Web: CSV, JSON, XML, HTML, RSS, Wiki\n• Multimedia: MP3, WAV, Images\n• URLs: YouTube, Website Links"
        if self.lang_key == "Türkçe":
             spec_text = "Desteklenen Formatlar:\n• Belgeler: PDF, DOCX, XLSX, PPTX\n• Veri & Web: CSV, JSON, XML, HTML, RSS, Wiki\n• Multimedya: MP3, WAV, Görsel\n• Bağlantılar: YouTube, Web Linkleri"
        view = FlyoutView(title=t["about_title"], content=f"{t['about_desc']}\n\n{spec_text}\n\n{t['about_dev']}: {DEVELOPER_NAME}\n{VERSION}\n\n{t['about_tech']}", icon=FIF.INFO)
        f_btn = PrimaryPushButton(FIF.GITHUB, "View Source")
        f_btn.setFixedWidth(140)
        f_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(GITHUB_URL)))
        view.addWidget(f_btn, align=Qt.AlignmentFlag.AlignRight)
        Flyout.make(view, self.info_btn, self, FlyoutAnimationType.PULL_UP)

    def detectLanguage(self):
        self.lang_key = "English"
        sys_locale = QLocale.system().name()
        if sys_locale.startswith("tr"): self.lang_key = "Türkçe"
        elif sys_locale.startswith("es"): self.lang_key = "Español"
        elif sys_locale.startswith("fr"): self.lang_key = "Français"
        elif sys_locale.startswith("de"): self.lang_key = "Deutsch"
        elif sys_locale.startswith("zh"): self.lang_key = "中文"
        self.lang_box.setCurrentText(self.lang_key)
        self.updateTexts()
        self.log(TRANSLATIONS[self.lang_key]["auto_detect"])

    def log(self, m, l="INFO"):
        time_str = datetime.now().strftime("%H:%M:%S")
        color = "#aaa"
        if l == "ERROR": color = "#ff4b4b"
        elif l == "SUCCESS": color = "#217346"
        self.log_area.append(f"<span style='color: #666;'>[{time_str}]</span> <span style='color: {color};'>{m}</span>")
        logging.info(m)

    def updateLang(self, lang):
        self.lang_key = lang
        self.updateTexts()

    def updateTexts(self):
        t = TRANSLATIONS[self.lang_key]
        self.title_label.setText(t["title"])
        self.sub_label.setText(t["subtitle"])
        self.info_label.setText(t["drop_text"])
        self.btn.setText(t["select_file"])
        self.log_header_label.setText(t["logs"])

    def selectFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select", "", "All Files (*)")
        if path: self.startWorker(path)

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls(): e.accept()
        else: e.ignore()

    def dropEvent(self, e: QDropEvent):
        files = [u.toLocalFile() for u in e.mimeData().urls()]
        if files: self.startWorker(files[0])

    def startWorker(self, path):
        self.pbar.setVisible(True)
        self.pbar.setRange(0, 0)
        self.btn.setEnabled(False)
        self.log(f"Process starting: {os.path.basename(path)}")
        self.worker = MarkItDownWorker(path)
        self.worker.finished.connect(self.done)
        self.worker.error.connect(self.fail)
        self.worker.start()

    def done(self, path):
        self.pbar.setVisible(False)
        self.btn.setEnabled(True)
        self.log(f"Saved: {os.path.basename(path)}", "SUCCESS")
        t = TRANSLATIONS[self.lang_key]
        InfoBar.success(t["success_title"], f"{t['success_msg']}\n{os.path.basename(path)}", duration=5000, parent=self)

    def fail(self, m):
        self.pbar.setVisible(False)
        self.btn.setEnabled(True)
        if "UnknownValueError" in m:
            m = "Audio conversion failed. Currently, only English is reliably supported, or the audio quality is too low."
            if self.lang_key == "Türkçe": m = "Ses dökümü başarısız. Şu an sadece İngilizce dil desteği stabildir veya ses kalitesi çok düşüktür."
        self.log(f"ERROR: {m}", "ERROR")
        t = TRANSLATIONS[self.lang_key]
        InfoBar.error(t["error_title"], m, duration=8000, parent=self)

if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    w = MarkItDownApp()
    w.show()
    sys.exit(app.exec())
