import React from 'react';
import './Home.css';
import axios from 'axios';

function Home() {
    const handleFetchData = async () => {
        try {
            // Replace these values with actual inputs or states as needed
            const low = 0;
            const high = 90000000;

            // Make the API call to Django backend
            const response = await axios.post(
                'http://localhost:8000/stockapi/fetch-screener-query-data/', { low, high });

            if (response.status === 200) {
                console.log("Data retrieved and saved successfully", response.data);
            } else {
                console.error("Failed to retrieve data:", response.data.error);
            }
        } catch (error) {
            console.error("An error occurred while fetching data:", error);
        }
    };

    return (
        <div className="home-container">
            <h1>Welcome to the Home Page</h1>
            <button className="fetch-data-button" onClick={handleFetchData}>
                Fetch Screener Query Data
            </button>
        </div>
    );
}

export default Home;
