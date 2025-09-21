import { useState } from 'react';
import { ToastContainer, toast, Slide } from 'react-toastify';
import axios from 'axios'
import './App.css'

const api = axios.create({
  baseURL: 'http://localhost:8080',
  timeout: 30000,
});

function App() {

  const [inputFile, setInputFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [operation, setOperation] = useState('analyze'); 
  const [language, setLanguage] = useState('en'); 

  function handleFileChange(e) {
    e.preventDefault();
    console.log(e);
    setInputFile(e.target.files[0] || null);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!inputFile) {
      toast.error("No file uploaded");
      return;
    };

    if (inputFile.size > 4 * 1024 * 1024) {
      toast.error("File too large");
      return;
    }


    const formData = new FormData();
    formData.append("file", inputFile);
    formData.append("language", language);

    setLoading(true);

    try {
      let response;
      if (operation === 'analyze') {
        response = await api.post('/api/v1/analyzer/upload_file', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        // Handle analysis response
        if (response.data.analysis) {
          const url = window.URL.createObjectURL(new Blob([JSON.stringify(response.data.analysis)], { type: 'application/json' }));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', `analyzed_${inputFile.name}.json`);
          document.body.appendChild(link);
          link.click();
          link.remove();
          toast.success("Analysis completed! File downloaded.");
        }
      } else if (operation === 'redact') {
        response = await api.post('/api/v1/redactor/upload_file', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          responseType: 'blob',
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `redacted_${inputFile.name}`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        toast.success("Redaction completed! File downloaded.");
      }
    } catch (error) {
      console.error('Upload error:', error);
      if (error.response) {
        toast.error(`Server error: ${error.response.data.detail || 'Unknown error'}`);
      } else if (error.request) {
        toast.error("Network error: Please check if the backend server is running");
      } else {
        toast.error("Upload failed: " + error.message);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick={false}
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
        transition={Slide}
      />
      <form className='main_app' onSubmit={handleSubmit}>
        <div className="heading">
          <h1>Privato</h1>
          <p>Analyze or redact sensitive information from your files</p>
        </div>

        <div className="operation-selector">
          <div
            className={`operation-option ${operation === 'analyze' ? 'selected' : ''}`}
            onClick={() => setOperation('analyze')}
          >
            Analyze File
          </div>
          <div
            className={`operation-option ${operation === 'redact' ? 'selected' : ''}`}
            onClick={() => setOperation('redact')}
          >
            Redact File
          </div>
          <div className="language-selector">
            <select
              id="language"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="de">German</option>
            </select>
          </div>
        </div>



        <div className='file-container'>
          <input type="file" name="userfile" id="userfile" onChange={handleFileChange} accept='.pdf,.csv,.txt,.png,.jpg,.jpeg,.tiff,.bmp,.xlsx,.json,application/pdf,text/csv,text/plain,image/*' />
          <label htmlFor="userfile">{`${inputFile ? inputFile.name : "Upload or Drop your File"}`}</label>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Submit'}
        </button>
      </form>
    </>
  );
}

export default App;
