import React, { useState, useEffect } from 'react';
import a from "../media/A.gif";
import b from "../media/B.gif";
import c from "../media/C.gif";
import d from "../media/D.gif";
import background from "../media/background.png";
import chore from "../media/video_compressed (2).mp4";
import Score from "./score";
import GifBar from './GifBar';
import ProgressBar from './progressBar';

const gifMap = {
    'A': a,
    'B': b,
    'C': c,
    'D': d,
    // Add more mappings as needed
};

export default function VideoFeed() {
    const [prediction, setPrediction] = useState(null);
    const [userScore, setUserScore] = useState(0);
    const [videoPosition, setVideoPosition] = useState(0);
    const [gif, setGif] = useState(background);
    const [videoDuration, setVideoDuration] = useState(0);

    useEffect(() => {
         
        const interval = setInterval(() => {
            fetch('/predict')
                .then(response => response.json())
                .then(data => {
                    if (data.prediction !== undefined) {
                        setPrediction(data.prediction);
                        setGif(gifMap[data.prediction]);
                        setUserScore(data.score);
                    }
                })
                .catch(error => console.error('Error fetching prediction:', error));
        }, 100); // Fetch prediction every second

        return () => clearInterval(interval);
    }, []);

    const handleVideoStart = () => {
        fetch('/video_started', { method: 'POST' })
            .then(response => response.json())
            .then(data => console.log('Video started:', data))
            .catch(error => console.error('Error sending video start request:', error));
    };

    const handleTimeUpdate = (event) => {
        const currentPosition = event.target.currentTime;
        setVideoPosition(currentPosition);
        fetch('/update_position', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ position: currentPosition }),
        })
            .then(response => response.json())
            .then(data => console.log('Position updated:', data))
            .catch(error => console.error('Error updating position:', error));
    };

    const [isVideoLoaded, setIsVideoLoaded] = useState(false);

    const handleLoadedData = () => {
        const videoElement = document.querySelector('video');
        if (videoElement) {
            setVideoDuration(videoElement.duration);
        }
        setIsVideoLoaded(true);
    };

    return (
        <div className="grid grid-cols-3 gap-4 p-4 items-stretch">
            <div className="col-span-2 flex flex-col items-center justify-between">
                <video
                    width="920"
                    height="640"
                    preload="auto"
                    onPlay={handleVideoStart}
                    onTimeUpdate={handleTimeUpdate}
                    onLoadedData={handleLoadedData}
                    className={`rounded-3xl mb-4 ${!isVideoLoaded ? 'opacity-50' : ''}`}
                >
                    <source src={chore} type="video/mp4" />
                </video>

                {!isVideoLoaded && <p className="text-gray-500 mb-4">Loading video...</p>}

                <ProgressBar score={Math.round(videoPosition / videoDuration * 100)} className="mb-4 p-7" />
            </div>

            <div className="flex flex-col items-center justify-between">
                <div className="mb-4">
                    <GifBar image={gif} prediction={prediction} />
                </div>
                <img src="/video_feed" alt="Prediction" className="h-64 rounded-3xl mb-4" />
                <div className="mb-4 flex-row">
                

                <div className="mb-4">
                    {prediction !== null && (
                        <div className="mb-4">
                            <Score score={Math.round((userScore / 18) * 10)} />
                        </div>
                    )}
                </div>
                <button
                    onClick={() => {
                        const videoElement = document.querySelector('video');
                        if (videoElement.paused) {
                            videoElement.play();
                        } else {
                            videoElement.pause();
                        }
                    }}
                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 mb-4">
                    Start Video
                </button>
                </div>
                <img src={a} alt="A" className="hidden" />
                <img src={b} alt="B" className="hidden" />
                <img src={c} alt="C" className="hidden" />
                <img src={d} alt="D" className="hidden" />
            </div>
        </div>
    );
}
