from flask import Flask, request, jsonify
from flask_cors import CORS
from markitdown import MarkItDown

app = Flask(__name__)
CORS(app)

markitdown = MarkItDown()

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' in request.files:
        file = request.files['file']
        result = markitdown.convert(file.stream, file_extension=file.filename.split('.')[-1])
        return jsonify({'content': result.text_content})
    elif 'url' in request.form:
        url = request.form['url']
        result = markitdown.convert(url)
        return jsonify({'content': result.text_content})
    else:
        return jsonify({'error': 'No file or URL provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
