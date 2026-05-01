document.addEventListener('DOMContentLoaded', function() {
    let convertedDocuments = [];
    let currentDocIndex = -1;
    let activeView = 'markdown';

    const elements = {
        uploadBtn: document.getElementById('uploadBtn'),
        emptyUploadBtn: document.getElementById('emptyUploadBtn'),
        fileInput: document.getElementById('fileInput'),
        settingsBtn: document.getElementById('settingsBtn'),
        settingsModal: document.getElementById('settingsModal'),
        closeSettingsBtn: document.getElementById('closeSettingsBtn'),
        modalOverlay: document.getElementById('modalOverlay'),
        processingTitle: document.getElementById('processingTitle'),
        processingFilename: document.getElementById('processingFilename'),
        progressInfo: document.getElementById('progressInfo'),
        progressCurrent: document.getElementById('progressCurrent'),
        progressTotal: document.getElementById('progressTotal'),
        previewHeader: document.getElementById('previewHeader'),
        viewToggle: document.getElementById('viewToggle'),
        emptyState: document.getElementById('emptyState'),
        resultContent: document.getElementById('resultContent'),
        previewFileIcon: document.getElementById('previewFileIcon'),
        previewFilename: document.getElementById('previewFilename'),
        previewFileType: document.getElementById('previewFileType'),
        markdownContent: document.getElementById('markdownContent'),
        previewContent: document.getElementById('previewContent'),
        markdownView: document.getElementById('markdownView'),
        previewView: document.getElementById('previewView'),
        toggleBtns: document.querySelectorAll('.toggle-btn'),
        copyBtn: document.getElementById('copyBtn'),
        downloadBtn: document.getElementById('downloadBtn'),
        sidebarActions: document.getElementById('sidebarActions'),
        batchDownloadBtn: document.getElementById('batchDownloadBtn'),
        clearAllBtn: document.getElementById('clearAllBtn'),
        documentList: document.getElementById('documentList'),
        emptyList: document.getElementById('emptyList'),
        llmConfigForm: document.getElementById('llmConfigForm'),
        apiKeyInput: document.getElementById('apiKeyInput'),
        baseUrlInput: document.getElementById('baseUrlInput'),
        modelInput: document.getElementById('modelInput'),
        toggleApiKey: document.getElementById('toggleApiKey'),
        clearConfigBtn: document.getElementById('clearConfigBtn'),
        toast: document.getElementById('toast'),
        toastMessage: document.getElementById('toastMessage'),
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

    function showProcessingModal() {
        elements.modalOverlay.hidden = false;
    }

    function hideProcessingModal() {
        elements.modalOverlay.hidden = true;
        elements.progressInfo.hidden = true;
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

    function switchView(view) {
        activeView = view;
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

    function displayDocument(doc) {
        if (!doc) {
            elements.previewHeader.hidden = true;
            elements.viewToggle.hidden = true;
            elements.emptyState.hidden = false;
            elements.resultContent.hidden = true;
            return;
        }

        elements.previewHeader.hidden = false;
        elements.viewToggle.hidden = false;
        elements.emptyState.hidden = true;
        elements.resultContent.hidden = false;

        const ext = doc.filename.split('.').pop().toLowerCase();
        
        elements.previewFileIcon.textContent = getFileIcon(ext);
        elements.previewFilename.textContent = doc.filename;
        elements.previewFileType.textContent = getFileTypeName(ext);

        elements.markdownContent.textContent = doc.markdown;

        const previewHtml = marked.parse(doc.markdown);
        elements.previewContent.innerHTML = previewHtml;

        switchView(activeView);
    }

    function updateDocumentList() {
        if (convertedDocuments.length === 0) {
            elements.emptyList.hidden = false;
            elements.sidebarActions.hidden = true;
            elements.documentList.innerHTML = '';
            elements.documentList.appendChild(elements.emptyList);
            displayDocument(null);
            return;
        }

        elements.emptyList.hidden = true;
        elements.sidebarActions.hidden = false;
        
        elements.documentList.innerHTML = '';
        
        convertedDocuments.forEach((doc, index) => {
            const ext = doc.filename.split('.').pop().toLowerCase();
            const item = document.createElement('div');
            item.className = `document-item ${doc.status || 'success'} ${index === currentDocIndex ? 'active' : ''}`;
            item.dataset.index = index;
            
            item.innerHTML = `
                <span class="document-item-icon">${getFileIcon(ext)}</span>
                <div class="document-item-details">
                    <span class="document-item-name">${doc.filename}</span>
                    <span class="document-item-status ${doc.status || 'success'}">
                        ${doc.status === 'error' ? doc.error : '已转换'}
                    </span>
                </div>
            `;
            
            item.addEventListener('click', () => {
                if (doc.status !== 'error') {
                    selectDocument(index);
                }
            });
            
            elements.documentList.appendChild(item);
        });
    }

    function selectDocument(index) {
        if (index < 0 || index >= convertedDocuments.length) return;
        
        currentDocIndex = index;
        
        document.querySelectorAll('.document-item').forEach((item, i) => {
            if (i === index) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
        
        const doc = convertedDocuments[index];
        if (doc && doc.status !== 'error') {
            displayDocument(doc);
        }
    }

    function openFileDialog() {
        elements.fileInput.click();
    }

    async function handleFiles(files) {
        if (!files || files.length === 0) return;
        
        if (files.length === 1) {
            elements.processingTitle.textContent = '正在处理...';
            elements.processingFilename.textContent = files[0].name;
            elements.progressInfo.hidden = true;
        } else {
            elements.processingTitle.textContent = '正在批量处理...';
            elements.processingFilename.textContent = `共 ${files.length} 个文件`;
            elements.progressInfo.hidden = false;
            elements.progressCurrent.textContent = '0';
            elements.progressTotal.textContent = files.length;
        }
        
        showProcessingModal();
        
        const formData = new FormData();
        for (let file of files) {
            formData.append('files', file);
        }
        
        try {
            const response = await fetch('/api/convert-batch', {
                method: 'POST',
                body: formData,
                credentials: 'include',
            });
            
            const data = await response.json();
            hideProcessingModal();
            
            if (data.success) {
                const newResults = data.results.map(r => ({ ...r, status: 'success' }));
                const newErrors = data.errors.map(e => ({ ...e, status: 'error' }));
                
                convertedDocuments = [...newResults, ...newErrors, ...convertedDocuments];
                updateDocumentList();
                
                const firstSuccess = newResults.find(r => r.status === 'success');
                if (firstSuccess) {
                    const firstIndex = convertedDocuments.findIndex(d => d.filename === firstSuccess.filename);
                    selectDocument(firstIndex);
                }
                
                if (data.success_count > 0) {
                    showToast(`成功转换 ${data.success_count} 个文件`, 'success');
                }
                if (data.error_count > 0) {
                    showToast(`${data.error_count} 个文件转换失败`, 'error');
                }
            } else {
                showToast(data.error || '转换失败', 'error');
            }
        } catch (error) {
            hideProcessingModal();
            showToast(error.message || '网络错误', 'error');
        }
    }

    async function copyToClipboard() {
        if (currentDocIndex < 0 || !convertedDocuments[currentDocIndex]) {
            showToast('没有可复制的内容', 'error');
            return;
        }
        
        const doc = convertedDocuments[currentDocIndex];
        try {
            await navigator.clipboard.writeText(doc.markdown);
            showToast('已复制到剪贴板', 'success');
        } catch (error) {
            showToast('复制失败', 'error');
        }
    }

    function downloadCurrentDocument() {
        if (currentDocIndex < 0 || !convertedDocuments[currentDocIndex]) {
            showToast('没有可下载的内容', 'error');
            return;
        }
        
        const doc = convertedDocuments[currentDocIndex];
        const blob = new Blob([doc.markdown], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = doc.filename.replace(/\.[^/.]+$/, '.md');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showToast('下载已开始', 'success');
    }

    async function downloadAllDocuments() {
        const successDocs = convertedDocuments.filter(d => d.status === 'success');
        if (successDocs.length === 0) {
            showToast('没有可下载的文档', 'error');
            return;
        }
        
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

    function clearAllDocuments() {
        convertedDocuments = [];
        currentDocIndex = -1;
        updateDocumentList();
        displayDocument(null);
        showToast('已清空列表', 'success');
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

    elements.uploadBtn.addEventListener('click', openFileDialog);
    elements.emptyUploadBtn.addEventListener('click', openFileDialog);
    elements.fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
        elements.fileInput.value = '';
    });

    elements.settingsBtn.addEventListener('click', openSettingsModal);
    elements.closeSettingsBtn.addEventListener('click', closeSettingsModal);

    elements.toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            switchView(btn.dataset.view);
        });
    });

    elements.copyBtn.addEventListener('click', copyToClipboard);
    elements.downloadBtn.addEventListener('click', downloadCurrentDocument);
    elements.batchDownloadBtn.addEventListener('click', downloadAllDocuments);
    elements.clearAllBtn.addEventListener('click', clearAllDocuments);

    elements.llmConfigForm.addEventListener('submit', saveLLMConfig);
    elements.toggleApiKey.addEventListener('click', toggleApiKeyVisibility);
    elements.clearConfigBtn.addEventListener('click', clearLLMConfig);

    elements.settingsModal.addEventListener('click', (e) => {
        if (e.target === elements.settingsModal) {
            closeSettingsModal();
        }
    });

    marked.setOptions({
        breaks: true,
        gfm: true,
    });

    displayDocument(null);
});
