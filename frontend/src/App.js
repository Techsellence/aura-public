import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Home from './components/Home';
import VisualiseCSV from './components/VisualiseCSV';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/home" element={<Home />} />
                <Route path="/visualise-csv" element={<VisualiseCSV />} />
                <Route path="*" element={<Navigate to="/home" />} />
            </Routes>
        </Router>
    );
}

export default App;
