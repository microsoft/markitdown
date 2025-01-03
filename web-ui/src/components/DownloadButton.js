import React from 'react';

function DownloadButton({ content, fileName }) {
  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([content], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = fileName.replace(/\.[^/.]+$/, "") + ".md";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <button onClick={handleDownload}>
      Download Markdown
    </button>
  );
}

export default DownloadButton;
