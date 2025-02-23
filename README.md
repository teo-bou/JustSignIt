# Just Sign It

Just Sign It is a web application designed to help users learn and practice sign language through interactive video tutorials and real-time feedback.

## Deliverable 
Business model Canva : [[Business Model Canva Just Sign it!.pdf]]
Slides : [[3 min Pitch Just Sign it ! .pdf]]


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Just Sign It leverages machine learning and computer vision to recognize hand gestures and provide feedback to users as they practice sign language. The application is built using React for the frontend and Flask for the backend.


## Installation

### Prerequisites

- Node.js
- npm
- Python 3.x
- pip

### Frontend Setup

1. Navigate to the `reactfront` directory:
    ```sh
    cd frontend
    ```

2. Install the dependencies:
    ```sh
    npm install
    ```

3. Start the development server:
    ```sh
    npm start
    ```

### Backend Setup

1. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

2. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Start the Flask server:
    ```sh
    python WebappTest.py
    ```

## Usage

1. Open your browser and navigate to `http://localhost:3000`.
2. Follow the on-screen instructions to start practicing sign language.
3. Use the video feed to see real-time predictions and feedback.


