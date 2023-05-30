import React, { useState, useEffect } from 'react';
import 'materialize-css/dist/css/materialize.min.css';
import M from 'materialize-css';
import './App.css';
import axios from 'axios';
import AudioPlayer from './AudioPlayer';

function App() {
  useEffect(() => {
    M.AutoInit();
  }, []);

  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    const formData = new FormData();
    formData.append('file', selectedFile);
    axios
      .post('http://127.0.0.1:5000/uploadPdf', formData)
      .then((res) => {
        console.log(res);
      })
      .catch((err) => console.log(err));
  };

  return (
    <div className="App container">
      <h1 className="blue-text">Welcome to My App</h1>
      <div className="file-field input-field">
        <div className="btn">
          <span>Choose File</span>
          <input type="file" onChange={handleFileChange} />
        </div>
        <div className="file-path-wrapper">
          <input className="file-path validate" type="text" />
        </div>
      </div>
      <button className="btn waves-effect waves-light" onClick={handleFileUpload}>
        Upload
        <i className="material-icons">cloud_upload</i>
      </button>
      <AudioPlayer />
    </div>
    
  );
}

export default App;