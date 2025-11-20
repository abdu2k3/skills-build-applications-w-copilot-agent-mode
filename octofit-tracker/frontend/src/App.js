
import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Use window.location for dynamic host, fallback to localhost
    let apiBase = window.location.hostname.includes('github.dev')
      ? window.location.origin.replace(/:\d+/, ':8000')
      : 'http://localhost:8000';
    fetch(`${apiBase}/api/activities/`)
      .then((res) => {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.json();
      })
      .then((data) => {
        setActivities(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="container mt-4">
      <h1>OctoFit Activities</h1>
      {loading && <p>Loading...</p>}
      {error && <p className="text-danger">Error: {error}</p>}
      {!loading && !error && (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>User</th>
              <th>Type</th>
              <th>Duration (min)</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {activities.map((a) => (
              <tr key={a._id}>
                <td>{a.user?.name || a.user}</td>
                <td>{a.type}</td>
                <td>{a.duration}</td>
                <td>{a.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
