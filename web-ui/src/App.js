import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import MarkdownPreview from './components/MarkdownPreview';
import DownloadButton from './components/DownloadButton';
import axios from 'axios';

function App() {
  const [markdownContent, setMarkdownContent] = useState('');
  const [fileName, setFileName] = useState('');

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/convert', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMarkdownContent(response.data.markdown);
      setFileName(file.name);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>MarkItDown Web UI</h1>
      </header>
      <main>
        <FileUpload onFileUpload={handleFileUpload} />
        <MarkdownPreview content={markdownContent} />
        <DownloadButton content={markdownContent} fileName={fileName} />
      </main>
    </div>
  );
}

export default App;
