import '../index.css';
import { useState, useRef, useEffect } from 'react';

function NotesDisplay({ content, onContentChange }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState(content);

  useEffect(() => {
    setEditContent(content);
  }, [content]);

  const handleSave = async () => {
    await onContentChange(editContent);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditContent(content);
    setIsEditing(false);
  };

  const formatContent = (text) => {
    const lines = text.split('\n');
    const formatted = [];
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // Chapter/Section headers (look for "Chapter" at start)
      if (line.match(/^Chapter\s+\d+(\.\d+)?/i)) {
        formatted.push(
          <h1 key={i} className="text-3xl font-bold text-gray-900 mt-6 mb-3">
            {line}
          </h1>
        );
      }
      // Subheaders (lines that end without punctuation and are relatively short)
      else if (line.trim() && line.length < 60 && !line.match(/[.!?]$/) && !line.startsWith('↳') && !line.startsWith('□') && i < lines.length - 1 && lines[i + 1].trim()) {
        // Check if next line is indented or starts with special char (suggests this is a header)
        if (lines[i + 1].startsWith('↳') || lines[i + 1].startsWith('□') || lines[i + 1].startsWith(' ')) {
          formatted.push(
            <h2 key={i} className="text-2xl font-bold text-gray-800 mt-5 mb-2">
              {line}
            </h2>
          );
        } else {
          formatted.push(<p key={i} className="text-gray-700 leading-relaxed my-2">{line || '\u00A0'}</p>);
        }
      }
      // Checkbox items (□)
      else if (line.startsWith('□')) {
        formatted.push(
          <div key={i} className="flex items-start gap-2 my-3">
            <span className="text-blue-600 font-bold text-lg">□</span>
            <p className="text-gray-800 font-semibold flex-1">{line.substring(1).trim()}</p>
          </div>
        );
      }
      // Indented items with arrow (↳)
      else if (line.trim().startsWith('↳')) {
        const content = line.trim().substring(1).trim();
        formatted.push(
          <div key={i} className="flex items-start gap-2 ml-6 my-1.5">
            <span className="text-purple-600 font-bold">→</span>
            <p className="text-gray-700 flex-1">{content}</p>
          </div>
        );
      }
      // EXAMPLE headers
      else if (line.match(/^EXAMPLE:/i)) {
        formatted.push(
          <div key={i} className="bg-blue-50 border-l-4 border-blue-500 p-3 my-4 rounded">
            <p className="font-bold text-blue-800">{line}</p>
          </div>
        );
      }
      // Numbered steps (lines starting with digits followed by parenthesis)
      else if (line.match(/^\d+\)/)) {
        formatted.push(
          <div key={i} className="ml-8 my-2">
            <p className="text-gray-800">{line}</p>
          </div>
        );
      }
      // Regular indented content (starts with spaces)
      else if (line.startsWith('   ') && line.trim()) {
        formatted.push(
          <p key={i} className="ml-8 text-gray-700 my-1 leading-relaxed">
            {line.trim()}
          </p>
        );
      }
      // Empty lines
      else if (!line.trim()) {
        formatted.push(<div key={i} className="h-2"></div>);
      }
      // Regular text
      else {
        formatted.push(
          <p key={i} className="text-gray-700 leading-relaxed my-2">
            {line}
          </p>
        );
      }
    }
    
    return formatted;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800">Your Converted Notes</h2>
        {!isEditing ? (
          <button
            onClick={() => setIsEditing(true)}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Edit
          </button>
        ) : (
          <div className="flex gap-2">
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
            >
              Cancel
            </button>
          </div>
        )}
      </div>

      {isEditing ? (
        <div className="space-y-3">
          <div className="bg-blue-50 border border-blue-200 rounded p-3 text-sm text-gray-700">
            <p className="font-semibold mb-2">Formatting tips:</p>
            <ul className="space-y-1 ml-4">
              <li>• Use ^ for superscript: x^2 → x²</li>
              <li>• Use _ for subscript: H_2O → H₂O</li>
              <li>• Use ** for bold: **bold** → <strong>bold</strong></li>
              <li>• Use / for italics: /italic/ → <em>italic</em></li>
            </ul>
          </div>
          <textarea
            value={editContent}
            onChange={(e) => setEditContent(e.target.value)}
            className="w-full h-96 p-4 border border-gray-300 rounded font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Edit your notes here..."
          />
        </div>
      ) : (
        <div className="bg-gray-50 rounded p-6 overflow-auto max-h-[600px]">
          {formatContent(content)}
        </div>
      )}
    </div>
  );
}

function LoadingSpinner({ message }) {
  return (
    <div className="mt-8 flex flex-col items-center">
      <div className="relative">
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-200"></div>
        <div className="animate-spin rounded-full h-16 w-16 border-4 border-t-blue-500 absolute top-0 left-0"></div>
      </div>
      <p className="mt-4 text-gray-600 font-medium">{message}</p>
    </div>
  );
}

export default function SquareAwayLanding() {
  const [files, setFiles] = useState([]);
  const [notesContent, setNotesContent] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const fileInputRef = useRef(null);

  const handleFiles = (selectedFiles) => {
    const imageFiles = Array.from(selectedFiles).filter(file =>
      file.type.startsWith('image/')
    );
    setFiles(imageFiles);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    handleFiles(e.target.files);
  };

  const handleUpload = async () => {
    if (files.length === 0) return;

    const formData = new FormData();
    files.forEach(file => formData.append('images', file));

    setIsProcessing(true);
    setLoadingMessage('Uploading images...');
    setNotesContent('');

    try {
      // Upload and extract text
      const response = await fetch('http://127.0.0.1:5000/extract-text', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Extraction successful:', result);
        
        // Use the extracted text directly from the API response
        setNotesContent(result.extracted_text);
        setIsProcessing(false);
        setLoadingMessage('');
        
      } else {
        alert('Error uploading file');
        setIsProcessing(false);
      }
    } catch (err) {
      console.error(err);
      alert('Error uploading file');
      setIsProcessing(false);
    }
  };

  const loadNotesContent = async () => {
    try {
      const response = await fetch('./results/results.txt');
      if (response.ok) {
        let text = await response.text();
        setNotesContent(text);
      } else {
        alert('Could not load notes file. Make sure the file exists in results/');
      }
    } catch (err) {
      console.error(err);
      alert('Error loading notes file');
    } finally {
      setIsProcessing(false);
      setLoadingMessage('');
    }
  };

  const handleNotesSave = async (newContent) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/save-changed-notes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          changedNotes: newContent,
          filename: 'results.txt'
        }),
      });
      
      if (response.ok) {
        setNotesContent(newContent);
        console.log('Notes saved successfully');
      } else {
        alert('Error saving notes');
      }
    } catch (err) {
      console.error('Error saving notes:', err);
      alert('Error saving notes');
    }
  };

  return (
    <div className="bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 min-h-screen flex flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Upload your Notes to Begin</h1>
      
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={handleClick}
        className="w-96 h-64 border-4 border-dashed border-blue-300 rounded-xl flex flex-col items-center justify-center cursor-pointer hover:bg-blue-100 transition-colors"
      >
        <p className="text-gray-500 mb-2">Drag & Drop your images here</p>
        <p className="text-gray-400 text-sm">or click to select files</p>
        <input
          type="file"
          multiple
          accept="image/*"
          ref={fileInputRef}
          className="hidden"
          onChange={handleFileChange}
        />
      </div>

      {files.length > 0 && !isProcessing && !notesContent && (
        <>
          <div className="mt-6 w-96 grid grid-cols-3 gap-4">
            {files.map((file, index) => (
              <div key={index} className="relative">
                <img
                  src={URL.createObjectURL(file)}
                  alt={file.name}
                  className="w-full h-24 object-cover rounded"
                />
              </div>
            ))}
          </div>
          <button
            onClick={handleUpload}
            className="mt-4 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-semibold"
          >
            Convert to Text
          </button>
        </>
      )}

      {isProcessing && <LoadingSpinner message={loadingMessage} />}

      {notesContent && !isProcessing && (
        <div className="mt-8 w-full max-w-4xl">
          <NotesDisplay 
            content={notesContent}
            onContentChange={handleNotesSave}
          />
        </div>
      )}
    </div>
  );
}