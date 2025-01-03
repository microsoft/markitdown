import React from 'react';
import ReactMarkdown from 'react-markdown';

function MarkdownPreview({ content }) {
  return (
    <div className="markdown-preview">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
}

export default MarkdownPreview;
