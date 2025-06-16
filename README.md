# BonesyPersonalHelper

A Raspberry Pi application built with Python, featuring a Next.js frontend for debugging and development.

## Backend Setup Instructions (Raspberry Pi)

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python src/main.py
   ```

## Frontend Setup Instructions

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Frontend Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Project Structure

- `src/` - Main Python application source code
- `frontend/` - Next.js frontend application
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Features

- Speech recognition and GPIO control (Raspberry Pi)
- Web-based frontend for debugging and development
- [Additional features will be added here]