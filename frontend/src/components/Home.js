import React, { useState } from 'react';
import './Home.css';
import axios from 'axios';

function Home() {
    const [loading, setLoading] = useState(false); // Loading state
    const [completed, setCompleted] = useState(false); // Completion state

    const handleFetchData = async () => {
        setLoading(true); // Set loading to true when the fetch starts
        setCompleted(false);

        try {
            // Replace these values with actual inputs or states as needed
            const low = 0;
            const high = 90000000;

            const apiHost = process.env.REACT_APP_API_HOST;
            console.log('Backend API Host: ' + apiHost);
            // Make the API call to Django backend
            const response = await axios.post(
                apiHost + '/stockapi/fetch-screener-query-data/', { low, high });

            if (response.status === 200) {
                console.log("Data retrieved and saved successfully", response.data);
                setCompleted(true); // Set the completion status to true
            } else {
                console.error("Failed to retrieve data:", response.data.error);
            }
        } catch (error) {
            console.error("An error occurred while fetching data:", error);
        } finally {
            setLoading(false); // Set loading to false after fetch completes
        }
    };

    return (
        <div className="home-container">
            <h1>Welcome to the Home Page</h1>
            <button className="fetch-data-button" onClick={handleFetchData}>
                Fetch Screener Query Data
            </button>
            {loading && <div className="loading-indicator">Please wait, fetching data...</div>}
            {completed && !loading && <div className="completed-message">Data fetch complete!</div>}
        </div>
    );
}

export default Home;
