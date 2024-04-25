import React from 'react';

const WeatherTable = ({ data }) => {
    return (
        <>
            <h1>Latest Data</h1>
            <table style={{ borderCollapse: 'collapse', marginTop: '10px' }}>
                <tbody>
                    <tr>
                        <td style={{ padding: '5px', border: '1px solid black', width: '150px' }}>
                            <strong>Temperature:</strong>
                        </td>
                        <td style={{ padding: '5px', border: '1px solid black', width: '150px' }}>
                            {data.temperature} °C
                        </td>
                    </tr>
                    <tr>
                        <td style={{ padding: '5px', border: '1px solid black', width: '150px' }}>
                            <strong>Humidity:</strong>
                        </td>
                        <td style={{ padding: '5px', border: '1px solid black', width: '150px' }}>
                            {data.humidity} %
                        </td>
                    </tr>
                    <tr>
                        <td style={{ padding: '5px', border: '1px solid black', width: '150px' }}>
                            <strong>Wind Speed:</strong>
                        </td>
                        <td style={{ padding: '5px', border: '1px solid black', width: '150px' }}>
                            {data.wind_speed} km/h
                        </td>
                    </tr>
                    <tr>
                        <td style={{ padding: '5px', border: '1px solid black', width: '150px' }}>
                            <strong>Cloud Cover:</strong>
                        </td>
                        <td style={{ padding: '5px', border: '1px solid black', width: '150px' }}>
                            {data.cloud_cover} %
                        </td>
                    </tr>
                    <tr>
                        <td style={{ padding: '5px', border: '1px solid black', width: '150px' }}>
                            <strong>Visibility:</strong>
                        </td>
                        <td style={{ padding: '5px', border: '1px solid black', width: '150px' }}>
                            {data.visibility} km
                        </td>
                    </tr>
                </tbody>
            </table>
        </>
    );
};

export default WeatherTable;
