// Filename - App.js

// Importing modules
import React from 'react'
import "./App.css";
import VideoFeed from './Pages/VideoFeed';
import Header from './Pages/Header';

function App() {
    

    return (
        
        <div className="App">
            <Header />

        <VideoFeed />
        </div>
    );
}

export default App;