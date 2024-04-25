import React, { useState, useEffect } from 'react';
import axios from 'axios';
import WeatherTable from './WeatherTable';
import TemperatureGraph from './TemperatureGraph';
import '../App.css';

const WeatherDashboard = () => {
    const [locations, setLocations] = useState([]);
    const [selectedLocation, setSelectedLocation] = useState('');
    const [weatherData, setWeatherData] = useState(null);
    const [temperatureData, setTemperatureData] = useState([]);
    const [selectedVariable, setSelectedVariable] = useState('temperature');

    useEffect(() => {
        axios.get('http://localhost:8000/locations/')
            .then(response => {
                setLocations(response.data);
            })
            .catch(error => console.error('Error fetching locations:', error));
    }, []);

    useEffect(() => {
        if (selectedLocation && selectedLocation !== "Select Location") {
            axios.get(`http://localhost:8000/latest_weather/${selectedLocation}`)
                .then(response => {
                    setWeatherData(response.data);
                })
                .catch(error => console.error('Error fetching weather data:', error));

            axios.get(`http://localhost:8000/last_n_rows/${selectedLocation}?n=500`)
                .then(response => {
                    setTemperatureData(response.data);
                })
                .catch(error => console.error('Error fetching temperature data:', error));
        } else {
            setWeatherData(null);
            setTemperatureData([]);
        }
    }, [selectedLocation]);

    const handleLocationChange = event => {
        setSelectedLocation(event.target.value);
    };

    const handleVariableChange = event => {
        setSelectedVariable(event.target.value);
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '50px' }}>
            <div>
                <select className="custom-select" value={selectedLocation} onChange={handleLocationChange}>
                    <option>Select Location</option>
                    {locations.map(location => (
                        <option key={location} value={location}>{location}</option>
                    ))}
                </select>
                {weatherData && <WeatherTable data={weatherData} />}
            </div>
            <div>
                <div>
                    {temperatureData.length > 0 && (
                        <select className="custom-select" value={selectedVariable} onChange={handleVariableChange}>
                            <option value="temperature">Temperature</option>
                            <option value="humidity">Humidity</option>
                            <option value="wind_speed">Wind Speed</option>
                            <option value="cloud_cover">Cloud Cover</option>
                            <option value="visibility">Visibility</option>
                        </select>
                    )}
                </div>
                {temperatureData.length > 0 && <TemperatureGraph data={temperatureData} variable={selectedVariable} />}
            </div>
        </div>
    );
};

export default WeatherDashboard;