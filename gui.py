import os
import tempfile
from pathlib import Path

from flask import Flask, request, jsonify, render_template
from markitdown import MarkItDown, UnsupportedFormatException, FileConversionException

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024  # 64 MB


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/convert/file", methods=["POST"])
def convert_file():
    if "file" not in request.files:
        return jsonify({"error": "Keine Datei übermittelt."}), 400

    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "Dateiname fehlt."}), 400

    suffix = Path(f.filename).suffix
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    try:
        f.save(tmp.name)
        tmp.close()
        result = MarkItDown().convert(tmp.name)
        return jsonify({
            "markdown": result.markdown or "",
            "title": result.title or f.filename,
        })
    except UnsupportedFormatException as e:
        return jsonify({"error": f"Format nicht unterstützt: {e}"}), 415
    except FileConversionException as e:
        return jsonify({"error": f"Konvertierung fehlgeschlagen: {e}"}), 422
    except Exception as e:
        return jsonify({"error": f"Unerwarteter Fehler: {e}"}), 500
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


@app.route("/api/convert/url", methods=["POST"])
def convert_url():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "Bitte eine gültige http:// oder https:// URL angeben."}), 400

    try:
        result = MarkItDown().convert(url)
        return jsonify({
            "markdown": result.markdown or "",
            "title": result.title or url,
        })
    except UnsupportedFormatException as e:
        return jsonify({"error": f"Format nicht unterstützt: {e}"}), 415
    except FileConversionException as e:
        return jsonify({"error": f"Konvertierung fehlgeschlagen: {e}"}), 422
    except Exception as e:
        return jsonify({"error": f"Unerwarteter Fehler: {e}"}), 500


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MarkItDown Web-UI")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    print(f"MarkItDown GUI läuft auf http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)
