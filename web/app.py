import os
import io
import tempfile
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from markitdown import MarkItDown
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'pptx', 'ppt', 'xlsx', 'xls', 
                      'jpg', 'jpeg', 'png', 'html', 'htm', 'csv', 'json', 
                      'xml', 'epub', 'txt', 'md', 'ipynb'}

md = MarkItDown(enable_plugins=False)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported'}), 400
    
    try:
        filename = secure_filename(file.filename)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = os.path.join(temp_dir, filename)
            file.save(temp_path)
            
            result = md.convert(temp_path)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'markdown': result.text_content,
                'file_type': filename.rsplit('.', 1)[1].lower()
            })
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/supported-formats', methods=['GET'])
def supported_formats():
    return jsonify({
        'formats': [
            {'ext': 'pdf', 'name': 'PDF Documents', 'icon': '📄'},
            {'ext': 'docx', 'name': 'Word Documents', 'icon': '📝'},
            {'ext': 'doc', 'name': 'Word Documents', 'icon': '📝'},
            {'ext': 'pptx', 'name': 'PowerPoint Presentations', 'icon': '📊'},
            {'ext': 'ppt', 'name': 'PowerPoint Presentations', 'icon': '📊'},
            {'ext': 'xlsx', 'name': 'Excel Spreadsheets', 'icon': '📈'},
            {'ext': 'xls', 'name': 'Excel Spreadsheets', 'icon': '📈'},
            {'ext': 'jpg', 'name': 'JPEG Images', 'icon': '🖼️'},
            {'ext': 'jpeg', 'name': 'JPEG Images', 'icon': '🖼️'},
            {'ext': 'png', 'name': 'PNG Images', 'icon': '🖼️'},
            {'ext': 'html', 'name': 'HTML Files', 'icon': '🌐'},
            {'ext': 'htm', 'name': 'HTML Files', 'icon': '🌐'},
            {'ext': 'csv', 'name': 'CSV Files', 'icon': '📋'},
            {'ext': 'json', 'name': 'JSON Files', 'icon': '📋'},
            {'ext': 'xml', 'name': 'XML Files', 'icon': '📋'},
            {'ext': 'epub', 'name': 'EPUB eBooks', 'icon': '📚'},
            {'ext': 'txt', 'name': 'Text Files', 'icon': '📄'},
            {'ext': 'md', 'name': 'Markdown Files', 'icon': '📝'},
            {'ext': 'ipynb', 'name': 'Jupyter Notebooks', 'icon': '📓'},
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
