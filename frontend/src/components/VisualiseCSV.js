import React, { useState } from 'react';
import '../VisualiseCSV.css';
import SimpleLineChart from "./SimpleLineChart";

function VisualiseCSV() {
    const [data, setData] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);
    const [keyword, setKeyword] = useState('');
    const [message, setMessage] = useState('');
    const fileInputRef = React.createRef();

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = () => {
        if (selectedFile) {
            const formData = new FormData();
            formData.append('file', selectedFile);

            fetch('http://localhost:8000/stockapi/upload/', {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    setData(data.data);
                    setMessage(''); // Clear any previous message
                })
                .catch(error => console.error('Error uploading file:', error));
        }
    };

    const handleSearch = () => {
        fetch(`http://localhost:8000/stockapi/search/?keyword=${keyword}`)
            .then(response => response.json())
            .then(data => {
                setData(data.data);
                if (data.data.length === 0) {
                    setMessage('No matching results found');
                } else {
                    setMessage(''); // Clear the message if results are found
                }
            })
            .catch(error => console.error('Error searching data:', error));
    };

    return (
        <div className="visualise-csv-container">
            <h1>CSV Upload</h1>
            <div className="button-container">
                <div
                    className="custom-file-input"
                    onClick={() => fileInputRef.current && fileInputRef.current.click()}
                >
                    Choose File
                </div>
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    style={{display: 'none'}}
                />
                <button onClick={handleUpload}>Upload</button>
            </div>
            <div className="search-container">
                <input
                    type="text"
                    placeholder="Enter keyword"
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    className="search-input"
                />
                <button onClick={handleSearch}>Search</button>
            </div>
            {message && <div className="message">{message}</div>}
            {data.length > 0 && (
                <div className="table-container">
                    <table>
                        <thead>
                        <tr>
                            {Object.keys(data[0]).map((key) => (
                                <th key={key}>{key}</th>
                            ))}
                        </tr>
                        </thead>
                        <tbody>
                        {data.map((row, index) => (
                            <tr key={index}>
                                {Object.values(row).map((value, i) => (
                                    <td key={i}>{value}</td>
                                ))}
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            )}
            {data.length > 0 && (
                <SimpleLineChart data={data}/>
            )}
        </div>
    );
}

export default VisualiseCSV;
