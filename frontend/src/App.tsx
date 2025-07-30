import React, { useState } from 'react';
import api from './api';

function App() {
  const [prompt, setPrompt] = useState('');
  const [jobId, setJobId] = useState('');
  const [status, setStatus] = useState('');
  const [videoUrl, setVideoUrl] = useState('');

  const submitJob = async () => {
    const response = await api.post('/api/jobs/submit', { prompt });
    setJobId(response.data.job_id);
    setStatus('submitted');
  };

  const checkStatus = async () => {
    if (!jobId) return;
    const response = await api.get(`/api/jobs/${jobId}`);
    setStatus(response.data.status);
    if (response.data.status === 'completed') {
      setVideoUrl(`/api/jobs/${jobId}/output`);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: 'Arial' }}>
      <h1>Text to Video Generator</h1>
      <input
        type="text"
        value={prompt}
        placeholder="Enter a prompt..."
        onChange={(e) => setPrompt(e.target.value)}
        style={{ width: 400, marginRight: 10 }}
      />
      <button onClick={submitJob}>Submit</button>

      {jobId && (
        <>
          <p>Job ID: {jobId}</p>
          <button onClick={checkStatus}>Check Status</button>
          <p>Status: {status}</p>
          {videoUrl && (
            <video controls width="500">
              <source src={videoUrl} type="video/mp4" />
            </video>
          )}
        </>
      )}
    </div>
  );
}

export default App;
