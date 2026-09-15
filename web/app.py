import os
import io
import tempfile
import zipfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session, send_file
from flask_cors import CORS
from markitdown import MarkItDown
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'markitdown-secret-key-2026'
CORS(app, supports_credentials=True)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'pptx', 'ppt', 'xlsx', 'xls', 
                      'jpg', 'jpeg', 'png', 'html', 'htm', 'csv', 'json', 
                      'xml', 'epub', 'txt', 'md', 'ipynb'}

def get_markitdown():
    llm_config = session.get('llm_config', {})
    kwargs = {'enable_plugins': False}
    
    if llm_config.get('api_key'):
        try:
            from openai import OpenAI
            
            client_kwargs = {'api_key': llm_config['api_key']}
            if llm_config.get('base_url'):
                client_kwargs['base_url'] = llm_config['base_url']
            
            client = OpenAI(**client_kwargs)
            kwargs['llm_client'] = client
            
            if llm_config.get('model'):
                kwargs['llm_model'] = llm_config['model']
        except ImportError:
            pass
    
    return MarkItDown(**kwargs)


def get_file_extension(filename):
    return Path(filename).suffix.lower().lstrip('.')


def allowed_file(filename):
    ext = get_file_extension(filename)
    return ext in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


def convert_single_file(file, md):
    original_filename = file.filename
    
    if not original_filename:
        return None, {'error': 'No filename', 'filename': original_filename}
    
    if not allowed_file(original_filename):
        return None, {'error': 'File type not supported', 'filename': original_filename}
    
    try:
        ext = get_file_extension(original_filename)
        
        safe_filename = secure_filename(original_filename)
        if not safe_filename or safe_filename == '.':
            safe_filename = f"upload.{ext}"
        elif not get_file_extension(safe_filename):
            safe_filename = f"{safe_filename}.{ext}"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = os.path.join(temp_dir, safe_filename)
            file.save(temp_path)
            
            result = md.convert(temp_path)
            
            return {
                'success': True,
                'filename': original_filename,
                'markdown': result.text_content,
                'file_type': ext
            }, None
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None, {'error': str(e), 'filename': original_filename}


@app.route('/api/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    md = get_markitdown()
    
    result, error = convert_single_file(file, md)
    
    if error:
        return jsonify(error), 400
    
    return jsonify(result)


@app.route('/api/convert-batch', methods=['POST'])
def convert_batch():
    if 'files' not in request.files:
        return jsonify({'error': 'No files part'}), 400
    
    files = request.files.getlist('files')
    
    if not files:
        return jsonify({'error': 'No selected files'}), 400
    
    md = get_markitdown()
    results = []
    errors = []
    
    for file in files:
        if file.filename:
            result, error = convert_single_file(file, md)
            if result:
                results.append(result)
            if error:
                errors.append(error)
    
    session['batch_results'] = results
    
    return jsonify({
        'success': True,
        'total': len(files),
        'success_count': len(results),
        'error_count': len(errors),
        'results': results,
        'errors': errors
    })


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


@app.route('/api/llm-config', methods=['GET', 'POST', 'DELETE'])
def llm_config():
    if request.method == 'GET':
        config = session.get('llm_config', {})
        return jsonify({
            'has_config': bool(config.get('api_key')),
            'model': config.get('model', ''),
            'base_url': config.get('base_url', ''),
        })
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data or not data.get('api_key'):
            return jsonify({'error': 'API key is required'}), 400
        
        session['llm_config'] = {
            'api_key': data.get('api_key'),
            'model': data.get('model', 'gpt-4o'),
            'base_url': data.get('base_url', ''),
        }
        
        return jsonify({
            'success': True,
            'message': 'LLM config saved successfully'
        })
    
    elif request.method == 'DELETE':
        session.pop('llm_config', None)
        return jsonify({
            'success': True,
            'message': 'LLM config cleared successfully'
        })


@app.route('/api/download-batch', methods=['GET'])
def download_batch():
    results = session.get('batch_results', [])
    
    if not results:
        return jsonify({'error': 'No batch results available'}), 400
    
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, 'converted_files.zip')
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for result in results:
                filename = result['filename']
                markdown = result['markdown']
                md_filename = os.path.splitext(filename)[0] + '.md'
                zipf.writestr(md_filename, markdown)
        
        return send_file(
            zip_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name='converted_files.zip'
        )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
