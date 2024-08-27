import React, { useState } from 'react';
import axios from 'axios';

function Upload({ onUpload }) {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);
        try {
            const apiHost = process.env.REACT_APP_API_HOST;
            const response = await axios.post(apiHost + '/stockapi/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            onUpload(response.data);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" onChange={handleFileChange} accept=".csv" />
            <button type="submit">Upload</button>
        </form>
    );
}

export default Upload;
