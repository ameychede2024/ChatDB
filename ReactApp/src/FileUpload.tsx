// FileUploader.tsx
import React, { useState, useRef } from 'react';
import axios from 'axios';
import './FileUpload.css';

interface FileUploaderProps {
  isOpen: boolean;
  onClose: () => void;
}

const FileUploader: React.FC<FileUploaderProps> = ({ isOpen, onClose }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault();
  };

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault();
    const file = event.dataTransfer.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);
    setUploading(true);

    try {
      await axios.post('http://localhost:5000/upload', formData, {
        onUploadProgress: (progressEvent) => {
          const progress = Math.round(
            (progressEvent.loaded * 100) / (progressEvent.total || 1)
          );
          setUploadProgress(progress);
        },
      });
      alert('File uploaded successfully!');
      setSelectedFile(null);
      setUploadProgress(0);
      onClose();
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Upload File</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        
        <div
          className="drop-zone"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            type="file"
            onChange={handleFileSelect}
            ref={fileInputRef}
            style={{ display: 'none' }}
          />
          {selectedFile ? (
            <div className="selected-file">
              <p>{selectedFile.name}</p>
              <span>({Math.round(selectedFile.size / 1024)} KB)</span>
            </div>
          ) : (
            <div className="upload-prompt">
              <i className="upload-icon">↑</i>
              <p>Drag and drop a file here or click to select</p>
            </div>
          )}
        </div>

        {uploading && (
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${uploadProgress}%` }}
            />
            <span>{uploadProgress}%</span>
          </div>
        )}

        <div className="modal-footer">
          <button 
            className="upload-button"
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default FileUploader;