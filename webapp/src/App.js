import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';

function App() {

  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/df').then(res => res.json()).then(data => {
      setCurrentTime(data.length);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>The current time iss {currentTime}.</p>
      </header>
    </div>
  );
}

export default App;
