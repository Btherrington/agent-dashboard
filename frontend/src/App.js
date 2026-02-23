import { useState, useEffect } from 'react';

function App() {
  const [commits, setCommits] = useState([]);
  const [generatedPost, setGeneratedPost] = useState("");
  const [postStatus, setPostStatus] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/stored-commits")
      .then(response => response.json())
      .then(data => setCommits(data));
  }, []);

  function generatePost() {
    fetch("http://127.0.0.1:8000/generate-post")
    .then(response => response.json())
    .then(data => setGeneratedPost(data))
  }
  function sendTweet() {
    fetch(`http://127.0.0.1:8000/post-tweet?text=${generatedPost}`,
      {method: "POST"})
      .then(response => response.json())
      .then(data => setPostStatus(data.status))
  }
  

  return (
    <div style={{backgroundColor: '#0f172a', minHeight: '100vh', padding: '32px', color: 'white', fontFamily: 'monospace'}}>
      <h1 style={{fontSize: '28px', fontWeight: 'bold', marginBottom: '8px'}}>Agent Dashboard</h1>
      <p style={{color: '#94a3b8', marginBottom: '32px'}}>GitHub Tracker Agent • {commits.length} commits tracked</p>
      
      <div style={{backgroundColor: '#1e293b', padding: '20px', borderRadius: '8px', marginBottom: '24px', borderLeft: '3px solid #10b981'}}>
  <h2 style={{fontSize: '20px', marginBottom: '12px'}}>Content Poster Agent</h2>
  
  <button onClick={generatePost} style={{backgroundColor: '#3b82f6', color: 'white', padding: '8px 16px', borderRadius: '6px', border: 'none', cursor: 'pointer', marginRight: '8px'}}>
    Generate Post
  </button>

  {generatedPost && (
    <>
      <p style={{color: '#e2e8f0', marginTop: '12px'}}>{generatedPost}</p>
      <button onClick={sendTweet} style={{backgroundColor: '#10b981', color: 'white', padding: '8px 16px', borderRadius: '6px', border: 'none', cursor: 'pointer', marginTop: '8px'}}>
        Post Tweet
      </button>
    </>
  )}

  {postStatus && (
    <p style={{color: postStatus === 'posted' ? '#10b981' : '#ef4444', marginTop: '8px'}}>
      Status: {postStatus}
    </p>
  )}
</div>

      <div style={{display: 'grid', gap: '12px'}}>
        {commits.map((commit, index) => (
          <div key={index} style={{backgroundColor: '#1e293b', padding: '16px', borderRadius: '8px', borderLeft: '3px solid #3b82f6'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
              <span style={{color: '#3b82f6', fontWeight: 'bold'}}>{commit.repo}</span>
              <span style={{color: '#64748b', fontSize: '12px'}}>{commit.date}</span>
            </div>
            <p style={{color: '#e2e8f0', marginTop: '4px'}}>{commit.message}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;