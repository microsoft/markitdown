document.addEventListener('DOMContentLoaded', function() {
    let currentMarkdown = '';
    let currentFilename = '';
    let selectedFiles = [];
    let batchResults = [];

    const elements = {
        uploadArea: document.getElementById('uploadArea'),
        fileInput: document.getElementById('fileInput'),
        selectFilesBtn: document.getElementById('selectFilesBtn'),
        uploadSection: document.getElementById('uploadSection'),
        resultSection: document.getElementById('resultSection'),
        batchResultSection: document.getElementById('batchResultSection'),
        modalOverlay: document.getElementById('modalOverlay'),
        processingFilename: document.getElementById('processingFilename'),
        processingTitle: document.getElementById('processingTitle'),
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
        toast: document.getElementById('toast'),
        toastMessage: document.getElementById('toastMessage'),
        toggleBtns: document.querySelectorAll('.toggle-btn'),
        fileListContainer: document.getElementById('fileListContainer'),
        fileList: document.getElementById('fileList'),
        selectedCount: document.getElementById('selectedCount'),
        clearFilesBtn: document.getElementById('clearFilesBtn'),
        convertAllBtn: document.getElementById('convertAllBtn'),
        settingsBtn: document.getElementById('settingsBtn'),
        settingsModal: document.getElementById('settingsModal'),
        closeSettingsBtn: document.getElementById('closeSettingsBtn'),
        llmConfigForm: document.getElementById('llmConfigForm'),
        apiKeyInput: document.getElementById('apiKeyInput'),
        baseUrlInput: document.getElementById('baseUrlInput'),
        modelInput: document.getElementById('modelInput'),
        toggleApiKey: document.getElementById('toggleApiKey'),
        clearConfigBtn: document.getElementById('clearConfigBtn'),
        batchSuccessCount: document.getElementById('batchSuccessCount'),
        batchErrorCount: document.getElementById('batchErrorCount'),
        batchResultsList: document.getElementById('batchResultsList'),
        batchDownloadAllBtn: document.getElementById('batchDownloadAllBtn'),
        batchNewFileBtn: document.getElementById('batchNewFileBtn'),
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

    function showToast(message, type = 'normal') {
        elements.toastMessage.textContent = message;
        elements.toast.className = 'toast';
        if (type === 'success') {
            elements.toast.classList.add('success');
        } else if (type === 'error') {
            elements.toast.classList.add('error');
        }
        elements.toast.classList.add('show');
        
        setTimeout(() => {
            elements.toast.classList.remove('show');
        }, 3000);
    }

    function showModal() {
        elements.modalOverlay.hidden = false;
    }

    function hideModal() {
        elements.modalOverlay.hidden = true;
    }

    function showSection(section) {
        elements.uploadSection.hidden = true;
        elements.resultSection.hidden = true;
        elements.batchResultSection.hidden = true;
        if (section) {
            section.hidden = false;
        }
    }

    function getFileIcon(extension) {
        return fileIcons[extension.toLowerCase()] || '📄';
    }

    function getFileTypeName(extension) {
        return fileTypeNames[extension.toLowerCase()] || 'Document';
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function updateFileList() {
        if (selectedFiles.length === 0) {
            elements.fileListContainer.hidden = true;
            elements.fileList.innerHTML = '';
            return;
        }

        elements.fileListContainer.hidden = false;
        elements.selectedCount.textContent = selectedFiles.length;
        elements.fileList.innerHTML = '';

        selectedFiles.forEach((file, index) => {
            const ext = file.name.split('.').pop().toLowerCase();
            const item = document.createElement('div');
            item.className = 'file-item';
            item.innerHTML = `
                <div class="file-item-info">
                    <span class="file-item-icon">${getFileIcon(ext)}</span>
                    <div class="file-item-details">
                        <span class="file-item-name">${file.name}</span>
                        <span class="file-item-size">${formatFileSize(file.size)}</span>
                    </div>
                </div>
                <button class="btn-icon btn-remove" data-index="${index}" title="移除">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </button>
            `;
            elements.fileList.appendChild(item);
        });

        document.querySelectorAll('.btn-remove').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = parseInt(btn.dataset.index);
                selectedFiles.splice(index, 1);
                updateFileList();
            });
        });
    }

    function handleFiles(files) {
        if (!files || files.length === 0) return;
        
        for (let file of files) {
            selectedFiles.push(file);
        }
        
        updateFileList();
    }

    async function uploadAndConvert(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                body: formData,
                credentials: 'include',
            });
            
            const data = await response.json();
            
            if (data.success) {
                return { success: true, data };
            } else {
                return { success: false, error: data.error || '转换失败' };
            }
        } catch (error) {
            return { success: false, error: error.message || '网络错误' };
        }
    }

    async function uploadAndConvertBatch() {
        if (selectedFiles.length === 0) {
            showToast('没有选择文件', 'error');
            return;
        }

        const formData = new FormData();
        selectedFiles.forEach(file => {
            formData.append('files', file);
        });

        elements.processingTitle.textContent = '正在批量处理...';
        elements.processingFilename.textContent = `共 ${selectedFiles.length} 个文件`;
        showModal();

        try {
            const response = await fetch('/api/convert-batch', {
                method: 'POST',
                body: formData,
                credentials: 'include',
            });
            
            const data = await response.json();
            hideModal();
            
            if (data.success) {
                batchResults = data.results;
                displayBatchResults(data);
                showToast(`批量转换完成：成功 ${data.success_count} 个，失败 ${data.error_count} 个`, 'success');
            } else {
                showToast(data.error || '批量转换失败', 'error');
            }
        } catch (error) {
            hideModal();
            showToast(error.message || '网络错误', 'error');
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

    function displayBatchResults(data) {
        elements.batchSuccessCount.textContent = data.success_count;
        elements.batchErrorCount.textContent = data.error_count;
        elements.batchResultsList.innerHTML = '';

        const allResults = [
            ...data.results.map(r => ({ ...r, status: 'success' })),
            ...data.errors.map(e => ({ ...e, status: 'error' }))
        ];

        allResults.forEach(result => {
            const ext = result.filename.split('.').pop().toLowerCase();
            const item = document.createElement('div');
            item.className = `batch-result-item ${result.status}`;
            
            if (result.status === 'success') {
                item.innerHTML = `
                    <div class="batch-result-info">
                        <span class="batch-result-icon">${getFileIcon(ext)}</span>
                        <div class="batch-result-details">
                            <span class="batch-result-name">${result.filename}</span>
                            <span class="batch-result-status success">转换成功</span>
                        </div>
                    </div>
                    <div class="batch-result-actions">
                        <button class="btn-ghost btn-small view-result-btn" data-filename="${result.filename}">
                            查看
                        </button>
                        <button class="btn-ghost btn-small download-single-btn" data-filename="${result.filename}">
                            下载
                        </button>
                    </div>
                `;
            } else {
                item.innerHTML = `
                    <div class="batch-result-info">
                        <span class="batch-result-icon">${getFileIcon(ext)}</span>
                        <div class="batch-result-details">
                            <span class="batch-result-name">${result.filename}</span>
                            <span class="batch-result-status error">${result.error}</span>
                        </div>
                    </div>
                `;
            }
            
            elements.batchResultsList.appendChild(item);
        });

        document.querySelectorAll('.view-result-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const filename = btn.dataset.filename;
                const result = batchResults.find(r => r.filename === filename);
                if (result) {
                    displayResult(result);
                }
            });
        });

        document.querySelectorAll('.download-single-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const filename = btn.dataset.filename;
                const result = batchResults.find(r => r.filename === filename);
                if (result) {
                    downloadSingleMarkdown(result);
                }
            });
        });

        showSection(elements.batchResultSection);
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
            showToast('已复制到剪贴板', 'success');
        } catch (error) {
            showToast('复制失败', 'error');
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
        showToast('下载已开始', 'success');
    }

    function downloadSingleMarkdown(result) {
        const blob = new Blob([result.markdown], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = result.filename.replace(/\.[^/.]+$/, '.md');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showToast('下载已开始', 'success');
    }

    async function downloadAllBatch() {
        try {
            const response = await fetch('/api/download-batch', {
                method: 'GET',
                credentials: 'include',
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'converted_files.zip';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                showToast('下载已开始', 'success');
            } else {
                const data = await response.json();
                showToast(data.error || '下载失败', 'error');
            }
        } catch (error) {
            showToast(error.message || '网络错误', 'error');
        }
    }

    function resetToUpload() {
        elements.fileInput.value = '';
        selectedFiles = [];
        batchResults = [];
        updateFileList();
        showSection(elements.uploadSection);
    }

    function openSettingsModal() {
        loadLLMConfig();
        elements.settingsModal.hidden = false;
    }

    function closeSettingsModal() {
        elements.settingsModal.hidden = true;
    }

    async function loadLLMConfig() {
        try {
            const response = await fetch('/api/llm-config', {
                method: 'GET',
                credentials: 'include',
            });
            
            const data = await response.json();
            
            if (data.has_config) {
                elements.baseUrlInput.value = data.base_url || '';
                elements.modelInput.value = data.model || 'gpt-4o';
            }
        } catch (error) {
            console.error('Failed to load LLM config:', error);
        }
    }

    async function saveLLMConfig(e) {
        e.preventDefault();
        
        const apiKey = elements.apiKeyInput.value.trim();
        if (!apiKey) {
            showToast('请输入 API Key', 'error');
            return;
        }
        
        const config = {
            api_key: apiKey,
            base_url: elements.baseUrlInput.value.trim(),
            model: elements.modelInput.value.trim() || 'gpt-4o',
        };
        
        try {
            const response = await fetch('/api/llm-config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(config),
                credentials: 'include',
            });
            
            const data = await response.json();
            
            if (data.success) {
                showToast('配置已保存', 'success');
                closeSettingsModal();
            } else {
                showToast(data.error || '保存失败', 'error');
            }
        } catch (error) {
            showToast(error.message || '网络错误', 'error');
        }
    }

    async function clearLLMConfig() {
        try {
            const response = await fetch('/api/llm-config', {
                method: 'DELETE',
                credentials: 'include',
            });
            
            const data = await response.json();
            
            if (data.success) {
                elements.apiKeyInput.value = '';
                elements.baseUrlInput.value = '';
                elements.modelInput.value = 'gpt-4o';
                showToast('配置已清除', 'success');
            }
        } catch (error) {
            showToast(error.message || '网络错误', 'error');
        }
    }

    function toggleApiKeyVisibility() {
        const isPassword = elements.apiKeyInput.type === 'password';
        elements.apiKeyInput.type = isPassword ? 'text' : 'password';
        
        const showIcon = elements.toggleApiKey.querySelector('.icon-show');
        const hideIcon = elements.toggleApiKey.querySelector('.icon-hide');
        
        if (isPassword) {
            showIcon.style.display = 'none';
            hideIcon.style.display = 'block';
        } else {
            showIcon.style.display = 'block';
            hideIcon.style.display = 'none';
        }
    }

    if (elements.selectFilesBtn) {
        elements.selectFilesBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            e.preventDefault();
            elements.fileInput.click();
        });
    }

    if (elements.uploadArea) {
        elements.uploadArea.addEventListener('click', (e) => {
            if (e.target === elements.selectFilesBtn || 
                elements.selectFilesBtn && elements.selectFilesBtn.contains(e.target)) {
                return;
            }
            elements.fileInput.click();
        });
    }

    if (elements.fileInput) {
        elements.fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });
    }

    if (elements.uploadArea) {
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
    }

    elements.toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            switchView(btn.dataset.view);
        });
    });

    if (elements.copyBtn) {
        elements.copyBtn.addEventListener('click', copyToClipboard);
    }

    if (elements.downloadBtn) {
        elements.downloadBtn.addEventListener('click', downloadMarkdown);
    }

    if (elements.newFileBtn) {
        elements.newFileBtn.addEventListener('click', resetToUpload);
    }

    if (elements.clearFilesBtn) {
        elements.clearFilesBtn.addEventListener('click', () => {
            selectedFiles = [];
            updateFileList();
        });
    }

    if (elements.convertAllBtn) {
        elements.convertAllBtn.addEventListener('click', uploadAndConvertBatch);
    }

    if (elements.settingsBtn) {
        elements.settingsBtn.addEventListener('click', openSettingsModal);
    }

    if (elements.closeSettingsBtn) {
        elements.closeSettingsBtn.addEventListener('click', closeSettingsModal);
    }

    if (elements.llmConfigForm) {
        elements.llmConfigForm.addEventListener('submit', saveLLMConfig);
    }

    if (elements.toggleApiKey) {
        elements.toggleApiKey.addEventListener('click', toggleApiKeyVisibility);
    }

    if (elements.clearConfigBtn) {
        elements.clearConfigBtn.addEventListener('click', clearLLMConfig);
    }

    if (elements.batchDownloadAllBtn) {
        elements.batchDownloadAllBtn.addEventListener('click', downloadAllBatch);
    }

    if (elements.batchNewFileBtn) {
        elements.batchNewFileBtn.addEventListener('click', resetToUpload);
    }

    elements.settingsModal.addEventListener('click', (e) => {
        if (e.target === elements.settingsModal) {
            closeSettingsModal();
        }
    });

    marked.setOptions({
        breaks: true,
        gfm: true,
    });

    showSection(elements.uploadSection);
});
