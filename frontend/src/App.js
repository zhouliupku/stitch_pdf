import './App.css';
import React, { useState } from 'react';
import axios from 'axios';

const BACKEND_API = " http://127.0.0.1:5000/api";
  

function App() {

  const [files, setFiles] = useState([]);
  
  const handleFileChange = (event) => {
    const fileList = event.target.files;
    setFiles([...files, ...fileList]);
  };

  const handleDelete = (index) => {
    const newFiles = [...files];
    newFiles.splice(index, 1);
    setFiles(newFiles);
  };

  const handleMerge = async () => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files[]', file);
    });
    try {
      await axios.post(BACKEND_API + '/upload', formData);
      window.location.href = BACKEND_API + '/download'; // Redirect to download endpoint
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <h1>PDF Merge</h1>
      <input type="file" onChange={handleFileChange} multiple/>
      <ul>
        {files.map((file, index) => (
          <li key={index}>
            {file.name}
            <button onClick={() => handleDelete(index)}>Delete</button>
          </li>
        ))}
      </ul>
      <button onClick={() => handleMerge()}>Merge Files</button>
    </div>
  );
}

export default App;
