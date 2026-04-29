let currentMarkdown = '';
let currentFilename = '';

const elements = {
    uploadArea: document.getElementById('uploadArea'),
    fileInput: document.getElementById('fileInput'),
    selectFilesBtn: document.getElementById('selectFilesBtn'),
    uploadSection: document.getElementById('uploadSection'),
    processingSection: document.getElementById('processingSection'),
    resultSection: document.getElementById('resultSection'),
    errorSection: document.getElementById('errorSection'),
    processingFilename: document.getElementById('processingFilename'),
    resultFilename: document.getElementById('resultFilename'),
    resultFileType: document.getElementById('resultFileType'),
    fileIcon: document.getElementById('fileIcon'),
    markdownContent: document.getElementById('markdownContent'),
    previewContent: document.getElementById('previewContent'),
    markdownView: document.getElementById('markdownView'),
    previewView: document.getElementById('previewView'),
    copyBtn: document.getElementById('copyBtn'),
    downloadBtn: document.getElementById('downloadBtn'),
    newFileBtn: document.getElementById('newFileBtn'),
    retryBtn: document.getElementById('retryBtn'),
    errorMessage: document.getElementById('errorMessage'),
    toast: document.getElementById('toast'),
    toastMessage: document.getElementById('toastMessage'),
    toggleBtns: document.querySelectorAll('.toggle-btn'),
};

const fileIcons = {
    pdf: '📄',
    docx: '📝',
    doc: '📝',
    pptx: '📊',
    ppt: '📊',
    xlsx: '📈',
    xls: '📈',
    jpg: '🖼️',
    jpeg: '🖼️',
    png: '🖼️',
    html: '🌐',
    htm: '🌐',
    csv: '📋',
    json: '📋',
    xml: '📋',
    epub: '📚',
    txt: '📄',
    md: '📝',
    ipynb: '📓',
};

const fileTypeNames = {
    pdf: 'PDF Document',
    docx: 'Word Document',
    doc: 'Word Document',
    pptx: 'PowerPoint Presentation',
    ppt: 'PowerPoint Presentation',
    xlsx: 'Excel Spreadsheet',
    xls: 'Excel Spreadsheet',
    jpg: 'JPEG Image',
    jpeg: 'JPEG Image',
    png: 'PNG Image',
    html: 'HTML File',
    htm: 'HTML File',
    csv: 'CSV File',
    json: 'JSON File',
    xml: 'XML File',
    epub: 'EPUB eBook',
    txt: 'Text File',
    md: 'Markdown File',
    ipynb: 'Jupyter Notebook',
};

function showToast(message) {
    elements.toastMessage.textContent = message;
    elements.toast.classList.add('show');
    
    setTimeout(() => {
        elements.toast.classList.remove('show');
    }, 3000);
}

function showSection(section) {
    elements.uploadSection.hidden = true;
    elements.processingSection.hidden = true;
    elements.resultSection.hidden = true;
    elements.errorSection.hidden = true;
    
    section.hidden = false;
}

function getFileIcon(extension) {
    return fileIcons[extension.toLowerCase()] || '📄';
}

function getFileTypeName(extension) {
    return fileTypeNames[extension.toLowerCase()] || 'Document';
}

function handleFiles(files) {
    if (!files || files.length === 0) return;
    
    const file = files[0];
    const extension = file.name.split('.').pop().toLowerCase();
    
    elements.processingFilename.textContent = file.name;
    showSection(elements.processingSection);
    
    uploadAndConvert(file);
}

async function uploadAndConvert(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData,
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResult(data);
        } else {
            showError(data.error || '转换失败');
        }
    } catch (error) {
        showError(error.message || '网络错误');
    }
}

function displayResult(data) {
    currentMarkdown = data.markdown;
    currentFilename = data.filename;
    
    const extension = data.file_type;
    
    elements.resultFilename.textContent = data.filename;
    elements.resultFileType.textContent = getFileTypeName(extension);
    elements.fileIcon.textContent = getFileIcon(extension);
    
    elements.markdownContent.textContent = data.markdown;
    
    const previewHtml = marked.parse(data.markdown);
    elements.previewContent.innerHTML = previewHtml;
    
    showSection(elements.resultSection);
}

function showError(message) {
    elements.errorMessage.textContent = message;
    showSection(elements.errorSection);
}

function switchView(view) {
    elements.toggleBtns.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.view === view) {
            btn.classList.add('active');
        }
    });
    
    if (view === 'markdown') {
        elements.markdownView.classList.add('active');
        elements.previewView.classList.remove('active');
    } else {
        elements.markdownView.classList.remove('active');
        elements.previewView.classList.add('active');
    }
}

async function copyToClipboard() {
    try {
        await navigator.clipboard.writeText(currentMarkdown);
        showToast('已复制到剪贴板');
    } catch (error) {
        showToast('复制失败');
    }
}

function downloadMarkdown() {
    const blob = new Blob([currentMarkdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = currentFilename.replace(/\.[^/.]+$/, '.md');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('下载已开始');
}

function resetToUpload() {
    elements.fileInput.value = '';
    showSection(elements.uploadSection);
}

elements.selectFilesBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    elements.fileInput.click();
});

elements.uploadArea.addEventListener('click', () => {
    elements.fileInput.click();
});

elements.fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

elements.uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    elements.uploadArea.classList.add('drag-over');
});

elements.uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    elements.uploadArea.classList.remove('drag-over');
});

elements.uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    elements.uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    handleFiles(files);
});

elements.toggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        switchView(btn.dataset.view);
    });
});

elements.copyBtn.addEventListener('click', copyToClipboard);
elements.downloadBtn.addEventListener('click', downloadMarkdown);
elements.newFileBtn.addEventListener('click', resetToUpload);
elements.retryBtn.addEventListener('click', resetToUpload);

marked.setOptions({
    breaks: true,
    gfm: true,
});
