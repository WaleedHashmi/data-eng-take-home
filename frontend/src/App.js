import React from 'react';
import './App.css';
import WeatherDashboard from './components/WeatherDashboard';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Weather Dashboard</h1>
      </header>
      <WeatherDashboard />
    </div>
  );
}

export default App;
