"use client";

import { useState } from 'react';
import axios from 'axios';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [data, setData] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleQuestionChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleSubmit = async () => {
    if (file && question) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('question', question);

      setLoading(true);
      try {
        const res = await axios.post('http://localhost:8000/process', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        setData(res.data.data);
        setResponse(res.data.response);
      } catch (error) {
        console.error('Error processing request:', error);
        setResponse('Error processing request');
      } finally {
        setLoading(false);
      }
    } else {
      console.error('File or question is missing');
      setResponse('Please provide both a file and a question.');
    }
  };

  return (
    <div>
      <h1>Upload CSV and Ask Question</h1>
      
      <input type="file" onChange={handleFileChange} />
      <input
        type="text"
        placeholder="Enter your question"
        value={question}
        onChange={handleQuestionChange}
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Processing...' : 'Submit'}
      </button>

      {data && (
        <div>
          <h2>Data from CSV:</h2>
          <pre>{data}</pre>
        </div>
      )}
      
      {response && (
        <div>
          <h2>Response from Backend:</h2>
          <pre>{response}</pre>
        </div>
      )}
    </div>
  );
}
