import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKAGES = ROOT.parent / "packages" / "markitdown" / "src"
if str(PACKAGES) not in sys.path:
    sys.path.insert(0, str(PACKAGES))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PySide6.QtWidgets import QApplication

from ui.main_window import StudioMainWindow


def main() -> int:
    if os.name == "nt":
        os.environ.setdefault("QT_QPA_PLATFORM", "windows")
    else:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ.setdefault("QT_QPA_PLATFORMTHEME", "windows")

    exiftool_path = ROOT / "tools" / "exiftool.exe"
    if exiftool_path.exists():
        os.environ.setdefault("EXIFTOOL_PATH", str(exiftool_path))

    font_dir_candidates = [
        str(Path(sys.prefix) / "Lib" / "site-packages" / "PySide6" / "lib" / "fonts"),
        r"C:\Windows\Fonts",
        r"C:/Windows/Fonts",
    ]
    for candidate in font_dir_candidates:
        if os.path.isdir(candidate):
            os.environ.setdefault("QT_QPA_FONTDIR", candidate)
            break

    app = QApplication(sys.argv)
    app.setApplicationName("MarkItDown Studio")
    app.setOrganizationName("Microsoft")
    app.setApplicationVersion("1.0.0")

    window = StudioMainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
